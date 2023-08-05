"""Provide a simple Bot object, mirroring Telegram API methods.

camelCase methods mirror API directly, while snake_case ones act as middlewares
    someway.

Usage
    ```
    import sys

    from davtelepot.bot import Bot

    from data.passwords import my_token, my_other_token

    long_polling_bot = Bot(token=my_token, database_url='my_db')
    webhook_bot = Bot(token=my_other_token, hostname='example.com',
                      certificate='path/to/certificate.pem',
                      database_url='my_other_db')

    @long_polling_bot.command('/foo')
    async def foo_command(bot, update, user_record):
        return "Bar!"

    @webhook_bot.command('/bar')
    async def bar_command(bot, update, user_record):
        return "Foo!"

    exit_state = Bot.run(
        local_host='127.0.0.5',
        port=8552
    )
    sys.exit(exit_state)
    ```
"""

# Standard library modules
import asyncio
from collections import OrderedDict
import datetime
import io
import inspect
import logging
import os
import re

# Third party modules
from aiohttp import web

# Project modules
from .api import TelegramBot, TelegramError
from .database import ObjectWithDatabase
from .languages import MultiLanguageObject
from .utilities import (
    escape_html_chars, extract, get_secure_key, make_inline_query_answer,
    make_lines_of_buttons, remove_html_tags
)

# Do not log aiohttp `INFO` and `DEBUG` levels
logging.getLogger('aiohttp').setLevel(logging.WARNING)


class Bot(TelegramBot, ObjectWithDatabase, MultiLanguageObject):
    """Simple Bot object, providing methods corresponding to Telegram bot API.

    Multiple Bot() instances may be run together, along with a aiohttp web app.
    """

    bots = []
    _path = '.'
    runner = None
    # TODO: find a way to choose port automatically by default
    # Setting port to 0 does not work unfortunately
    local_host = 'localhost'
    port = 3000
    final_state = 0
    _maintenance_message = ("I am currently under maintenance!\n"
                            "Please retry later...")
    _authorization_denied_message = None
    _unknown_command_message = None
    TELEGRAM_MESSAGES_MAX_LEN = 4096
    _default_inline_query_answer = [
        dict(
            type='article',
            id=0,
            title="I cannot answer this query, sorry",
            input_message_content=dict(
                message_text="I'm sorry "
                "but I could not find an answer for your query."
            )
        )
    ]
    _log_file_name = None
    _errors_file_name = None

    def __init__(
        self, token, hostname='', certificate=None, max_connections=40,
        allowed_updates=[], database_url='bot.db'
    ):
        """Init a bot instance.

        token : str
            Telegram bot API token.
        hostname : str
            Domain (or public IP address) for webhooks.
        certificate : str
            Path to domain certificate.
        max_connections : int (1 - 100)
            Maximum number of HTTPS connections allowed.
        allowed_updates : List(str)
            Allowed update types (empty list to allow all).
        """
        # Append `self` to class list of instances
        self.__class__.bots.append(self)
        # Call superclasses constructors with proper arguments
        TelegramBot.__init__(self, token)
        ObjectWithDatabase.__init__(self, database_url=database_url)
        MultiLanguageObject.__init__(self)
        self._path = None
        self.preliminary_tasks = []
        self.final_tasks = []
        self._offset = 0
        self._hostname = hostname
        self._certificate = certificate
        self._max_connections = max_connections
        self._allowed_updates = allowed_updates
        self._session_token = get_secure_key(length=10)
        self._name = None
        self._telegram_id = None
        # The following routing table associates each type of Telegram `update`
        #   with a Bot method to be invoked on it.
        self.routing_table = {
            'message': self.message_router,
            'edited_message': self.edited_message_handler,
            'channel_post': self.channel_post_handler,
            'edited_channel_post': self.edited_channel_post_handler,
            'inline_query': self.inline_query_handler,
            'chosen_inline_result': self.chosen_inline_result_handler,
            'callback_query': self.callback_query_handler,
            'shipping_query': self.shipping_query_handler,
            'pre_checkout_query': self.pre_checkout_query_handler,
            'poll': self.poll_handler,
        }
        # Different message update types need different handlers
        self.message_handlers = {
            'text': self.text_message_handler,
            'audio': self.audio_message_handler,
            'document': self.document_message_handler,
            'animation': self.animation_message_handler,
            'game': self.game_message_handler,
            'photo': self.photo_message_handler,
            'sticker': self.sticker_message_handler,
            'video': self.video_message_handler,
            'voice': self.voice_message_handler,
            'video_note': self.video_note_message_handler,
            'contact': self.contact_message_handler,
            'location': self.location_message_handler,
            'venue': self.venue_message_handler,
            'poll': self.poll_message_handler,
            'new_chat_members': self.new_chat_members_message_handler,
            'left_chat_member': self.left_chat_member_message_handler,
            'new_chat_title': self.new_chat_title_message_handler,
            'new_chat_photo': self.new_chat_photo_message_handler,
            'delete_chat_photo': self.delete_chat_photo_message_handler,
            'group_chat_created': self.group_chat_created_message_handler,
            'supergroup_chat_created': (
                self.supergroup_chat_created_message_handler
            ),
            'channel_chat_created': self.channel_chat_created_message_handler,
            'migrate_to_chat_id': self.migrate_to_chat_id_message_handler,
            'migrate_from_chat_id': self.migrate_from_chat_id_message_handler,
            'pinned_message': self.pinned_message_message_handler,
            'invoice': self.invoice_message_handler,
            'successful_payment': self.successful_payment_message_handler,
            'connected_website': self.connected_website_message_handler,
            'passport_data': self.passport_data_message_handler
        }
        # Special text message handlers: individual, commands, aliases, parsers
        self.individual_text_message_handlers = dict()
        self.commands = OrderedDict()
        self.command_aliases = OrderedDict()
        self.messages['commands'] = dict()
        self.messages['reply_keyboard_buttons'] = dict()
        self._unknown_command_message = None
        self.text_message_parsers = OrderedDict()
        # Support for /help command
        self.messages['help_sections'] = OrderedDict()
        # Handle location messages
        self.individual_location_handlers = dict()
        # Callback query-related properties
        self.callback_handlers = OrderedDict()
        self._callback_data_separator = None
        # Inline query-related properties
        self.inline_query_handlers = OrderedDict()
        self._default_inline_query_answer = None
        self.chosen_inline_result_handlers = dict()
        # Maintenance properties
        self._under_maintenance = False
        self._allowed_during_maintenance = []
        self._maintenance_message = None
        # Default chat_id getter: same chat as update
        self.get_chat_id = lambda update: (
            update['message']['chat']['id']
            if 'message' in update and 'chat' in update['message']
            else update['chat']['id']
            if 'chat' in update
            else None
        )
        # Message to be returned if user is not allowed to call method
        self._authorization_denied_message = None
        # Default authorization function (always return True)
        self.authorization_function = (
            lambda update, user_record=None, authorization_level='user': True
        )
        self.default_reply_keyboard_elements = []
        self.recent_users = OrderedDict()
        self._log_file_name = None
        self._errors_file_name = None
        return

    @property
    def path(self):
        """Path where files should be looked for.

        If no instance path is set, return class path.
        """
        return self._path or self.__class__._path

    @classmethod
    def set_class_path(csl, path):
        """Set class path attribute."""
        csl._path = path

    def set_path(self, path):
        """Set instance path attribute."""
        self._path = path

    @property
    def log_file_name(self):
        """Return log file name.

        Fallback to class file name if set, otherwise return None.
        """
        return self._log_file_name or self.__class__._log_file_name

    @property
    def log_file_path(self):
        """Return log file path basing on self.path and `_log_file_name`.

        Fallback to class file if set, otherwise return None.
        """
        if self.log_file_name:
            return f"{self.path}/data/{self.log_file_name}"

    def set_log_file_name(self, file_name):
        """Set log file name."""
        self._log_file_name = file_name

    @classmethod
    def set_class_log_file_name(cls, file_name):
        """Set class log file name."""
        cls._log_file_name = file_name

    @property
    def errors_file_name(self):
        """Return errors file name.

        Fallback to class file name if set, otherwise return None.
        """
        return self._errors_file_name or self.__class__._errors_file_name

    @property
    def errors_file_path(self):
        """Return errors file path basing on self.path and `_errors_file_name`.

        Fallback to class file if set, otherwise return None.
        """
        if self.errors_file_name:
            return f"{self.path}/data/{self.errors_file_name}"

    def set_errors_file_name(self, file_name):
        """Set errors file name."""
        self._errors_file_name = file_name

    @classmethod
    def set_class_errors_file_name(cls, file_name):
        """Set class errors file name."""
        cls._errors_file_name = file_name

    @classmethod
    def get(cls, token, *args, **kwargs):
        """Given a `token`, return class instance with that token.

        If no instance is found, instantiate it.
        Positional and keyword arguments may be passed as well.
        """
        for bot in cls.bots:
            if bot.token == token:
                return bot
        return cls(token, *args, **kwargs)

    @property
    def hostname(self):
        """Hostname for the webhook URL.

        It must be a public domain or IP address. Port may be specified.
        A custom webhook url, including bot token and a random token, will be
        generated for Telegram to post new updates.
        """
        return self._hostname

    @property
    def webhook_url(self):
        """URL where Telegram servers should post new updates.

        It must be a public domain name or IP address. Port may be specified.
        """
        if not self.hostname:
            return ''
        return (
            f"{self.hostname}/webhook/{self.token}_{self.session_token}/"
        )

    @property
    def webhook_local_address(self):
        """Local address where Telegram updates are routed by revers proxy."""
        return (
            f"/webhook/{self.token}_{self.session_token}/"
        )

    @property
    def certificate(self):
        """Public certificate for `webhook_url`.

        May be self-signed
        """
        return self._certificate

    @property
    def max_connections(self):
        """Maximum number of simultaneous HTTPS connections allowed.

        Telegram will open as many connections as possible to boost bot’s
            throughput, lower values limit the load on bot‘s server.
        """
        return self._max_connections

    @property
    def allowed_updates(self):
        """List of update types to be retrieved.

        Empty list to allow all updates.
        """
        return self._allowed_updates

    @property
    def name(self):
        """Bot name."""
        return self._name

    @property
    def telegram_id(self):
        """Telegram id of this bot."""
        return self._telegram_id

    @property
    def session_token(self):
        """Return a token generated with the current instantiation."""
        return self._session_token

    @property
    def offset(self):
        """Return last update id.

        Useful to ignore repeated updates and restore original update order.
        """
        return self._offset

    @property
    def under_maintenance(self):
        """Return True if bot is under maintenance.

        While under maintenance, bot will reply `self.maintenance_message` to
            any update, except those which `self.is_allowed_during_maintenance`
            returns True for.
        """
        return self._under_maintenance

    @property
    def allowed_during_maintenance(self):
        """Return the list of criteria to allow an update during maintenance.

        If any of this criteria returns True on an update, that update will be
            handled even during maintenance.
        """
        return self._allowed_during_maintenance

    @property
    def maintenance_message(self):
        """Message to be returned if bot is under maintenance.

        If instance message is not set, class message is returned.
        """
        if self._maintenance_message:
            return self._maintenance_message
        if self.__class__.maintenance_message:
            return self.__class__._maintenance_message
        return ("I am currently under maintenance!\n"
                "Please retry later...")

    @property
    def authorization_denied_message(self):
        """Return this text if user is unauthorized to make a request.

        If instance message is not set, class message is returned.
        """
        if self._authorization_denied_message:
            return self._authorization_denied_message
        return self.__class__._authorization_denied_message

    def get_keyboard(self, user_record=dict(), update=dict(),
                     telegram_id=None):
        """Return a reply keyboard translated into user language."""
        if (not user_record) and telegram_id:
            with self.db as db:
                user_record = db['users'].find_one(telegram_id=telegram_id)
        buttons = [
            dict(
                text=self.get_message(
                    'reply_keyboard_buttons', command,
                    user_record=user_record, update=update,
                    default_message=element['reply_keyboard_button']
                )
            )
            for command, element in self.commands.items()
            if 'reply_keyboard_button' in element
        ]
        if len(buttons) == 0:
            return
        return dict(
            keyboard=make_lines_of_buttons(
                buttons,
                (2 if len(buttons) < 4 else 3)  # Row length
            ),
            resize_keyboard=True
        )

    @property
    def unknown_command_message(self):
        """Message to be returned if user sends an unknown command.

        If instance message is not set, class message is returned.
        """
        if self._unknown_command_message:
            message = self._unknown_command_message
        else:
            message = self.__class__._unknown_command_message
        if message is not None:
            message = message.format(bot=self)
        return message

    @property
    def callback_data_separator(self):
        """Separator between callback data elements.

        Example of callback_data: 'my_button_prefix:///1|4|test'
            Prefix: `my_button_prefix:///`
            Separator: `|` <--- this is returned
            Data: `['1', '4', 'test']`
        """
        return self._callback_data_separator

    def set_callback_data_separator(self, separator):
        """Set a callback_data separator.

        See property `callback_data_separator` for details.
        """
        assert type(separator) is str, "Separator must be a string!"
        self._callback_data_separator = separator

    @property
    def default_inline_query_answer(self):
        """Answer to be returned if inline query returned None.

        If instance default answer is not set, class one is returned.
        """
        if self._default_inline_query_answer:
            return self._default_inline_query_answer
        return self.__class__._default_inline_query_answer

    @classmethod
    def set_class_default_inline_query_answer(cls,
                                              default_inline_query_answer):
        """Set class default inline query answer.

        It will be returned if an inline query returned no answer.
        """
        cls._default_inline_query_answer = make_inline_query_answer(
            default_inline_query_answer
        )

    def set_default_inline_query_answer(self, default_inline_query_answer):
        """Set a custom default_inline_query_answer.

        It will be returned when no answer is found for an inline query.
        If instance answer is None, default class answer is used.
        """
        self._default_inline_query_answer = make_inline_query_answer(
            default_inline_query_answer
        )

    async def message_router(self, update, user_record):
        """Route Telegram `message` update to appropriate message handler."""
        for key, value in update.items():
            if key in self.message_handlers:
                return await self.message_handlers[key](update, user_record)
        logging.error(
            f"The following message update was received: {update}\n"
            "However, this message type is unknown."
        )

    async def edited_message_handler(self, update, user_record):
        """Handle Telegram `edited_message` update."""
        logging.info(
            f"The following update was received: {update}\n"
            "However, this edited_message handler does nothing yet."
        )
        return

    async def channel_post_handler(self, update, user_record):
        """Handle Telegram `channel_post` update."""
        logging.info(
            f"The following update was received: {update}\n"
            "However, this channel_post handler does nothing yet."
        )
        return

    async def edited_channel_post_handler(self, update, user_record):
        """Handle Telegram `edited_channel_post` update."""
        logging.info(
            f"The following update was received: {update}\n"
            "However, this edited_channel_post handler does nothing yet."
        )
        return

    async def inline_query_handler(self, update, user_record):
        """Handle Telegram `inline_query` update.

        Answer it with results or log errors.
        """
        query = update['query']
        results, switch_pm_text, switch_pm_parameter = None, None, None
        for condition, handler in self.inline_query_handlers.items():
            if condition(query):
                _handler = handler['handler']
                results = await _handler(bot=self, update=update,
                                         user_record=user_record)
                break
        if not results:
            results = self.default_inline_query_answer
        if type(results) is dict and 'answer' in results:
            if 'switch_pm_text' in results:
                switch_pm_text = results['switch_pm_text']
            if 'switch_pm_parameter' in results:
                switch_pm_parameter = results['switch_pm_parameter']
            results = results['answer']
        try:
            await self.answer_inline_query(
                update=update,
                results=results,
                cache_time=10,
                is_personal=True,
                switch_pm_text=switch_pm_text,
                switch_pm_parameter=switch_pm_parameter
            )
        except Exception as e:
            logging.info("Error answering inline query\n{}".format(e))
        return

    async def chosen_inline_result_handler(self, update, user_record):
        """Handle Telegram `chosen_inline_result` update."""
        if user_record is not None:
            user_id = user_record['telegram_id']
        else:
            user_id = update['from']['id']
        if user_id in self.chosen_inline_result_handlers:
            result_id = update['result_id']
            handlers = self.chosen_inline_result_handlers[user_id]
            if result_id in handlers:
                await handlers[result_id](update)
        return

    def set_chosen_inline_result_handler(self, user_id, result_id, handler):
        """Associate a `handler` to a `result_id` for `user_id`.

        When an inline result is chosen having that id, `handler` will
            be called and passed the update as argument.
        """
        if type(user_id) is dict:
            user_id = user_id['from']['id']
        assert type(user_id) is int, "user_id must be int!"
        # Query result ids are parsed as str by telegram
        result_id = str(result_id)
        assert callable(handler), "Handler must be callable"
        if user_id not in self.chosen_inline_result_handlers:
            self.chosen_inline_result_handlers[user_id] = {}
        self.chosen_inline_result_handlers[user_id][result_id] = handler
        return

    async def callback_query_handler(self, update, user_record):
        """Handle Telegram `callback_query` update.

        A callback query is sent when users press inline keyboard buttons.
        Bad clients may send malformed or deceiving callback queries:
            never put secrets in buttons and always check request validity!
        Get an `answer` from the callback handler associated to the query
            prefix and use it to edit the source message (or send new ones
            if text is longer than single message limit).
        Anyway, the query is answered, otherwise the client would hang and
            the bot would look like idle.
        """
        assert 'data' in update, "Malformed callback query lacking data field."
        answer = dict()
        data = update['data']
        for start_text, handler in self.callback_handlers.items():
            if data.startswith(start_text):
                _function = handler['handler']
                answer = await _function(
                    bot=self,
                    update=update,
                    user_record=user_record
                )
                break
        if answer is None:
            answer = ''
        if type(answer) is str:
            answer = dict(text=answer)
        assert type(answer) is dict, "Invalid callback query answer."
        if 'edit' in answer:
            message_identifier = self.get_message_identifier(update)
            edit = answer['edit']
            method = (
                self.edit_message_text if 'text' in edit
                else self.editMessageCaption if 'caption' in edit
                else self.editMessageReplyMarkup if 'reply_markup' in edit
                else (lambda *args, **kwargs: None)
            )
            try:
                await method(**message_identifier, **edit)
            except TelegramError as e:
                logging.info("Message was not modified:\n{}".format(e))
        try:
            return await self.answerCallbackQuery(
                callback_query_id=update['id'],
                **{
                    key: (val[:180] if key == 'text' else val)
                    for key, val in answer.items()
                    if key in ('text', 'show_alert', 'cache_time')
                }
            )
        except TelegramError as e:
            logging.error(e)
        return

    async def shipping_query_handler(self, update, user_record):
        """Handle Telegram `shipping_query` update."""
        logging.info(
            f"The following update was received: {update}\n"
            "However, this shipping_query handler does nothing yet."
        )
        return

    async def pre_checkout_query_handler(self, update, user_record):
        """Handle Telegram `pre_checkout_query` update."""
        logging.info(
            f"The following update was received: {update}\n"
            "However, this pre_checkout_query handler does nothing yet."
        )
        return

    async def poll_handler(self, update, user_record):
        """Handle Telegram `poll` update."""
        logging.info(
            f"The following update was received: {update}\n"
            "However, this poll handler does nothing yet."
        )
        return

    async def text_message_handler(self, update, user_record):
        """Handle `text` message update."""
        replier, reply = None, None
        text = update['text'].lower()
        user_id = update['from']['id'] if 'from' in update else None
        if user_id in self.individual_text_message_handlers:
            replier = self.individual_text_message_handlers[user_id]
            del self.individual_text_message_handlers[user_id]
        elif text.startswith('/'):  # Handle commands
            # A command must always start with the ‘/’ symbol and may not be
            # longer than 32 characters.
            # Commands can use latin letters, numbers and underscores.
            command = re.search(
                r"([A-z_1-9]){1,32}",  # Command pattern (without leading `/`)
                text
            ).group(0)  # Get the first group of characters matching pattern
            if command in self.commands:
                replier = self.commands[command]['handler']
            elif 'chat' in update and update['chat']['id'] > 0:
                reply = self.unknown_command_message
        else:  # Handle command aliases and text parsers
            # Aliases are case insensitive: text and alias are both .lower()
            for alias, function in self.command_aliases.items():
                if text.startswith(alias.lower()):
                    replier = function
                    break
            # Text message update parsers
            for check_function, parser in self.text_message_parsers.items():
                if (
                    parser['argument'] == 'text'
                    and check_function(text)
                ) or (
                    parser['argument'] == 'update'
                    and check_function(update)
                ):
                    replier = parser['handler']
                    break
        if replier:
            reply = await replier(
                bot=self,
                update=update,
                user_record=user_record
            )
        if reply:
            if type(reply) is str:
                reply = dict(text=reply)
            try:
                return await self.reply(update=update, **reply)
            except Exception as e:
                logging.error(
                    f"Failed to handle text message:\n{e}",
                    exc_info=True
                )
        return

    async def audio_message_handler(self, update, user_record):
        """Handle `audio` message update."""
        logging.info(
            "A audio message update was received, "
            "but this handler does nothing yet."
        )

    async def document_message_handler(self, update, user_record):
        """Handle `document` message update."""
        logging.info(
            "A document message update was received, "
            "but this handler does nothing yet."
        )

    async def animation_message_handler(self, update, user_record):
        """Handle `animation` message update."""
        logging.info(
            "A animation message update was received, "
            "but this handler does nothing yet."
        )

    async def game_message_handler(self, update, user_record):
        """Handle `game` message update."""
        logging.info(
            "A game message update was received, "
            "but this handler does nothing yet."
        )

    async def photo_message_handler(self, update, user_record):
        """Handle `photo` message update."""
        logging.info(
            "A photo message update was received, "
            "but this handler does nothing yet."
        )

    async def sticker_message_handler(self, update, user_record):
        """Handle `sticker` message update."""
        logging.info(
            "A sticker message update was received, "
            "but this handler does nothing yet."
        )

    async def video_message_handler(self, update, user_record):
        """Handle `video` message update."""
        logging.info(
            "A video message update was received, "
            "but this handler does nothing yet."
        )

    async def voice_message_handler(self, update, user_record):
        """Handle `voice` message update."""
        logging.info(
            "A voice message update was received, "
            "but this handler does nothing yet."
        )

    async def video_note_message_handler(self, update, user_record):
        """Handle `video_note` message update."""
        logging.info(
            "A video_note message update was received, "
            "but this handler does nothing yet."
        )

    async def contact_message_handler(self, update, user_record):
        """Handle `contact` message update."""
        logging.info(
            "A contact message update was received, "
            "but this handler does nothing yet."
        )

    async def location_message_handler(self, update, user_record):
        """Handle `location` message update."""
        replier, reply = None, None
        user_id = update['from']['id'] if 'from' in update else None
        if user_id in self.individual_location_handlers:
            replier = self.individual_location_handlers[user_id]
            del self.individual_location_handlers[user_id]
        if replier:
            reply = await replier(
                bot=self,
                update=update,
                user_record=user_record
            )
        if reply:
            if type(reply) is str:
                reply = dict(text=reply)
            try:
                return await self.reply(update=update, **reply)
            except Exception as e:
                logging.error(
                    f"Failed to handle location message:\n{e}",
                    exc_info=True
                )
        return

    async def venue_message_handler(self, update, user_record):
        """Handle `venue` message update."""
        logging.info(
            "A venue message update was received, "
            "but this handler does nothing yet."
        )

    async def poll_message_handler(self, update, user_record):
        """Handle `poll` message update."""
        logging.info(
            "A poll message update was received, "
            "but this handler does nothing yet."
        )

    async def new_chat_members_message_handler(self, update, user_record):
        """Handle `new_chat_members` message update."""
        logging.info(
            "A new_chat_members message update was received, "
            "but this handler does nothing yet."
        )

    async def left_chat_member_message_handler(self, update, user_record):
        """Handle `left_chat_member` message update."""
        logging.info(
            "A left_chat_member message update was received, "
            "but this handler does nothing yet."
        )

    async def new_chat_title_message_handler(self, update, user_record):
        """Handle `new_chat_title` message update."""
        logging.info(
            "A new_chat_title message update was received, "
            "but this handler does nothing yet."
        )

    async def new_chat_photo_message_handler(self, update, user_record):
        """Handle `new_chat_photo` message update."""
        logging.info(
            "A new_chat_photo message update was received, "
            "but this handler does nothing yet."
        )

    async def delete_chat_photo_message_handler(self, update, user_record):
        """Handle `delete_chat_photo` message update."""
        logging.info(
            "A delete_chat_photo message update was received, "
            "but this handler does nothing yet."
        )

    async def group_chat_created_message_handler(self, update, user_record):
        """Handle `group_chat_created` message update."""
        logging.info(
            "A group_chat_created message update was received, "
            "but this handler does nothing yet."
        )

    async def supergroup_chat_created_message_handler(self, update,
                                                      user_record):
        """Handle `supergroup_chat_created` message update."""
        logging.info(
            "A supergroup_chat_created message update was received, "
            "but this handler does nothing yet."
        )

    async def channel_chat_created_message_handler(self, update, user_record):
        """Handle `channel_chat_created` message update."""
        logging.info(
            "A channel_chat_created message update was received, "
            "but this handler does nothing yet."
        )

    async def migrate_to_chat_id_message_handler(self, update, user_record):
        """Handle `migrate_to_chat_id` message update."""
        logging.info(
            "A migrate_to_chat_id message update was received, "
            "but this handler does nothing yet."
        )

    async def migrate_from_chat_id_message_handler(self, update, user_record):
        """Handle `migrate_from_chat_id` message update."""
        logging.info(
            "A migrate_from_chat_id message update was received, "
            "but this handler does nothing yet."
        )

    async def pinned_message_message_handler(self, update, user_record):
        """Handle `pinned_message` message update."""
        logging.info(
            "A pinned_message message update was received, "
            "but this handler does nothing yet."
        )

    async def invoice_message_handler(self, update, user_record):
        """Handle `invoice` message update."""
        logging.info(
            "A invoice message update was received, "
            "but this handler does nothing yet."
        )

    async def successful_payment_message_handler(self, update, user_record):
        """Handle `successful_payment` message update."""
        logging.info(
            "A successful_payment message update was received, "
            "but this handler does nothing yet."
        )

    async def connected_website_message_handler(self, update, user_record):
        """Handle `connected_website` message update."""
        logging.info(
            "A connected_website message update was received, "
            "but this handler does nothing yet."
        )

    async def passport_data_message_handler(self, update, user_record):
        """Handle `passport_data` message update."""
        logging.info(
            "A passport_data message update was received, "
            "but this handler does nothing yet."
        )

    @staticmethod
    def split_message_text(text, limit=None, parse_mode='HTML'):
        r"""Split text if it hits telegram limits for text messages.

        Split at `\n` if possible.
        Add a `[...]` at the end and beginning of split messages,
        with proper code markdown.
        """
        if parse_mode == 'HTML':
            text = escape_html_chars(text)
        tags = (
            ('`', '`')
            if parse_mode == 'Markdown'
            else ('<code>', '</code>')
            if parse_mode.lower() == 'html'
            else ('', '')
        )
        if limit is None:
            limit = Bot.TELEGRAM_MESSAGES_MAX_LEN - 100
        # Example text: "lines\nin\nreversed\order"
        text = text.split("\n")[::-1]  # ['order', 'reversed', 'in', 'lines']
        text_part_number = 0
        while len(text) > 0:
            temp = []
            text_part_number += 1
            while (
                len(text) > 0
                and len(
                    "\n".join(temp + [text[-1]])
                ) < limit
            ):
                # Append lines of `text` in order (`.pop` returns the last
                # line in text) until the addition of the next line would hit
                # the `limit`.
                temp.append(text.pop())
            # If graceful split failed (last line was longer than limit)
            if len(temp) == 0:
                # Force split last line
                temp.append(text[-1][:limit])
                text[-1] = text[-1][limit:]
            text_chunk = "\n".join(temp)  # Re-join this group of lines
            prefix, suffix = '', ''
            is_last = len(text) == 0
            if text_part_number > 1:
                prefix = f"{tags[0]}[...]{tags[1]}\n"
            if not is_last:
                suffix = f"\n{tags[0]}[...]{tags[1]}"
            yield (prefix + text_chunk + suffix), is_last
        return

    async def reply(self, update=None, *args, **kwargs):
        """Reply to `update` with proper method according to `kwargs`."""
        method = None
        if 'text' in kwargs:
            if 'message_id' in kwargs:
                method = self.edit_message_text
            else:
                method = self.send_message
        elif 'photo' in kwargs:
            method = self.send_photo
        if method is not None:
            return await method(update=update, *args, **kwargs)
        raise Exception("Unsopported keyword arguments for `Bot().reply`.")

    async def send_message(self, chat_id=None, text=None,
                           parse_mode='HTML',
                           disable_web_page_preview=None,
                           disable_notification=None,
                           reply_to_message_id=None,
                           reply_markup=None,
                           update=dict(),
                           reply_to_update=False,
                           send_default_keyboard=True):
        """Send text via message(s).

        This method wraps lower-level `TelegramBot.sendMessage` method.
        Pass an `update` to extract `chat_id` and `message_id` from it.
        Set `reply_to_update` = True to reply to `update['message_id']`.
        Set `send_default_keyboard` = False to avoid sending default keyboard
            as reply_markup (only those messages can be edited, which were
            sent with no reply markup or with an inline keyboard).
        """
        if 'message' in update:
            update = update['message']
        if chat_id is None and 'chat' in update:
            chat_id = self.get_chat_id(update)
        if reply_to_update and 'message_id' in update:
            reply_to_message_id = update['message_id']
        if (
            send_default_keyboard
            and reply_markup is None
            and type(chat_id) is int
            and chat_id > 0
            and text != self.authorization_denied_message
        ):
            reply_markup = self.get_keyboard(
                update=update,
                telegram_id=chat_id
            )
        if not text:
            return
        parse_mode = str(parse_mode)
        text_chunks = self.split_message_text(
            text=text,
            limit=self.__class__.TELEGRAM_MESSAGES_MAX_LEN - 100,
            parse_mode=parse_mode
        )
        for text_chunk, is_last in text_chunks:
            _reply_markup = (reply_markup if is_last else None)
            sent_message_update = await self.sendMessage(
                chat_id=chat_id,
                text=text_chunk,
                parse_mode=parse_mode,
                disable_web_page_preview=disable_web_page_preview,
                disable_notification=disable_notification,
                reply_to_message_id=reply_to_message_id,
                reply_markup=_reply_markup
            )
        return sent_message_update

    async def edit_message_text(self, text,
                                chat_id=None, message_id=None,
                                inline_message_id=None,
                                parse_mode='HTML',
                                disable_web_page_preview=None,
                                reply_markup=None,
                                update=None):
        """Edit message text, sending new messages if necessary.

        This method wraps lower-level `TelegramBot.editMessageText` method.
        Pass an `update` to extract a message identifier from it.
        """
        if update is not None:
            message_identifier = self.get_message_identifier(update)
            if 'chat_id' in message_identifier:
                chat_id = message_identifier['chat_id']
                message_id = message_identifier['message_id']
            if 'inline_message_id' in message_identifier:
                inline_message_id = message_identifier['inline_message_id']
        for i, (text_chunk, is_last) in enumerate(
            self.split_message_text(
                text=text,
                limit=self.__class__.TELEGRAM_MESSAGES_MAX_LEN - 200,
                parse_mode=parse_mode
            )
        ):
            if i == 0:
                edited_message = await self.editMessageText(
                    text=text_chunk,
                    chat_id=chat_id,
                    message_id=message_id,
                    inline_message_id=inline_message_id,
                    parse_mode=parse_mode,
                    disable_web_page_preview=disable_web_page_preview,
                    reply_markup=(reply_markup if is_last else None)
                )
                if chat_id is None:
                    # Cannot send messages without a chat_id
                    # Inline keyboards attached to inline query results may be
                    # in chats the bot cannot reach.
                    break
                updates = [update]
            else:
                updates.append(
                    await self.send_message(
                        text=text_chunk,
                        chat_id=chat_id,
                        parse_mode=parse_mode,
                        disable_web_page_preview=disable_web_page_preview,
                        reply_markup=(reply_markup if is_last else None),
                        update=updates[-1],
                        reply_to_update=True,
                        send_default_keyboard=False
                    )
                )
        return edited_message

    async def forward_message(self, chat_id, update=None, from_chat_id=None,
                              message_id=None, disable_notification=False):
        """Forward message from `from_chat_id` to `chat_id`.

        Set `disable_notification` to True to avoid disturbing recipient.
        Pass the `update` to be forwarded or its identifier (`from_chat_id` and
            `message_id`).
        """
        if from_chat_id is None or message_id is None:
            message_identifier = self.get_message_identifier(update)
            from_chat_id = message_identifier['chat_id']
            message_id = message_identifier['message_id']
        return await self.forwardMessage(
            chat_id=chat_id,
            from_chat_id=from_chat_id,
            message_id=message_id,
            disable_notification=disable_notification,
        )

    async def delete_message(self, update=dict(), chat_id=None,
                             message_id=None):
        """Delete given update with given *args and **kwargs.

        Please note, that a bot can delete only messages sent by itself
        or sent in a group which it is administrator of.
        """
        if chat_id is None or message_id is None:
            message_identifier = self.get_message_identifier(update)
        else:
            message_identifier = dict(
                chat_id=chat_id,
                message_id=message_id
            )
        return await self.deleteMessage(
            **message_identifier
        )

    async def send_photo(self, chat_id=None, photo=None,
                         caption=None,
                         parse_mode=None,
                         disable_notification=None,
                         reply_to_message_id=None,
                         reply_markup=None,
                         update=dict(),
                         reply_to_update=False,
                         send_default_keyboard=True,
                         use_stored_file_id=True):
        """Send photos.

        This method wraps lower-level `TelegramBot.sendPhoto` method.
        Pass an `update` to extract `chat_id` and `message_id` from it.
        Set `reply_to_update` = True to reply to `update['message_id']`.
        Set `send_default_keyboard` = False to avoid sending default keyboard
            as reply_markup (only those messages can be edited, which were
            sent with no reply markup or with an inline keyboard).
        If photo was already sent by this bot and `use_stored_file_id` is set
            to True, use file_id (it is faster and recommended).
        """
        already_sent = False
        if 'message' in update:
            update = update['message']
        if chat_id is None and 'chat' in update:
            chat_id = self.get_chat_id(update)
        if reply_to_update and 'message_id' in update:
            reply_to_message_id = update['message_id']
        if (
            send_default_keyboard
            and reply_markup is None
            and type(chat_id) is int
            and chat_id > 0
            and caption != self.authorization_denied_message
        ):
            reply_markup = self.get_keyboard(
                update=update,
                telegram_id=chat_id
            )
        if type(photo) is str:
            photo_path = photo
            with self.db as db:
                already_sent = db['sent_pictures'].find_one(
                    path=photo_path,
                    errors=False
                )
            if already_sent and use_stored_file_id:
                photo = already_sent['file_id']
                already_sent = True
            else:
                already_sent = False
                if not any(
                    [
                            photo.startswith(url_starter)
                            for url_starter in ('http', 'www',)
                        ]
                ):  # If `photo` is not a url but a local file path
                    try:
                        with io.BytesIO() as buffered_picture:
                            with open(
                                os.path.join(self.path, photo_path),
                                'rb'  # Read bytes
                            ) as photo_file:
                                buffered_picture.write(photo_file.read())
                            photo = buffered_picture.getvalue()
                    except FileNotFoundError:
                        photo = None
        else:
            use_stored_file_id = False
        if photo is None:
            logging.error("Photo is None, `send_photo` returning...")
            return
        sent_update = None
        try:
            sent_update = await self.sendPhoto(
                chat_id=chat_id,
                photo=photo,
                caption=caption,
                parse_mode=parse_mode,
                disable_notification=disable_notification,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup
            )
            if isinstance(sent_update, Exception):
                raise Exception("sendPhoto API call failed!")
        except Exception as e:
            logging.error(f"Error sending photo\n{e}")
            if already_sent:
                with self.db as db:
                    db['sent_pictures'].update(
                        dict(
                            path=photo_path,
                            errors=True
                        ),
                        ['path']
                    )
        if (
            type(sent_update) is dict
            and 'photo' in sent_update
            and len(sent_update['photo']) > 0
            and 'file_id' in sent_update['photo'][0]
            and (not already_sent)
            and use_stored_file_id
        ):
            with self.db as db:
                db['sent_pictures'].insert(
                    dict(
                        path=photo_path,
                        file_id=sent_update['photo'][0]['file_id'],
                        errors=False
                    )
                )
        return sent_update

    async def send_document(self, chat_id=None, document=None, thumb=None,
                            caption=None, parse_mode=None,
                            disable_notification=None,
                            reply_to_message_id=None, reply_markup=None,
                            document_path=None,
                            document_name=None,
                            update=dict(),
                            reply_to_update=False,
                            send_default_keyboard=True,
                            use_stored_file_id=False):
        """Send a document.

        This method wraps lower-level `TelegramBot.sendDocument` method.
        Pass an `update` to extract `chat_id` and `message_id` from it.
        Set `reply_to_update` = True to reply to `update['message_id']`.
        Set `send_default_keyboard` = False to avoid sending default keyboard
            as reply_markup (only those messages can be edited, which were
            sent with no reply markup or with an inline keyboard).
        If document was already sent by this bot and `use_stored_file_id` is
            set to True, use file_id (it is faster and recommended).
        `document_path` may contain `{path}`: it will be replaced by
            `self.path`.
        `document_name` diplayed to Telegram may differ from actual document
            name if this parameter is set.
        """
        already_sent = False
        # This buffered_file trick is necessary for two reasons
        # 1. File operations must be blocking, but sendDocument is a coroutine
        # 2. A `with` statement is not possible here
        # `buffered_file` must be closed at all costs!
        buffered_file = None
        if 'message' in update:
            update = update['message']
        if chat_id is None and 'chat' in update:
            chat_id = self.get_chat_id(update)
        if reply_to_update and 'message_id' in update:
            reply_to_message_id = update['message_id']
        if (
            send_default_keyboard
            and reply_markup is None
            and type(chat_id) is int
            and chat_id > 0
            and caption != self.authorization_denied_message
        ):
            reply_markup = self.get_keyboard(
                update=update,
                telegram_id=chat_id,
            )
        if document_path is not None:
            with self.db as db:
                already_sent = db['sent_documents'].find_one(
                    path=document_path,
                    errors=False
                )
            if already_sent and use_stored_file_id:
                document = already_sent['file_id']
                already_sent = True
            else:
                already_sent = False
                if not any(
                    [
                            document_path.startswith(url_starter)
                            for url_starter in ('http', 'www',)
                        ]
                ):  # If `document_path` is not a url but a local file path
                    try:
                        with open(
                            document_path.format(
                                path=self.path
                            ),
                            'rb'  # Read bytes
                        ) as file_:
                            buffered_file = io.BytesIO(file_.read())
                            buffered_file.name = (
                                document_name
                                or file_.name
                                or 'Document'
                            )
                            document = buffered_file
                    except FileNotFoundError as e:
                        if buffered_file:
                            buffered_file.close()
                        return e
        else:
            use_stored_file_id = False
        if document is None:
            logging.error(
                "`document` is None, `send_document` returning..."
            )
            return Exception("No `document` provided")
        sent_update = None
        try:
            sent_update = await self.sendDocument(
                chat_id=chat_id,
                document=document,
                thumb=thumb,
                caption=caption,
                parse_mode=parse_mode,
                disable_notification=disable_notification,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup
            )
            if isinstance(sent_update, Exception):
                raise Exception("sendDocument API call failed!")
        except Exception as e:
            logging.error(f"Error sending document\n{e}")
            if already_sent:
                with self.db as db:
                    db['sent_documents'].update(
                        dict(
                            path=document_path,
                            errors=True
                        ),
                        ['path']
                    )
        finally:
            if buffered_file:
                buffered_file.close()
        if (
            type(sent_update) is dict
            and 'document' in sent_update
            and 'file_id' in sent_update['document']
            and (not already_sent)
            and use_stored_file_id
        ):
            with self.db as db:
                db['sent_documents'].insert(
                    dict(
                        path=document_path,
                        file_id=sent_update['document']['file_id'],
                        errors=False
                    )
                )
        return sent_update

    async def answer_inline_query(self,
                                  inline_query_id=None,
                                  results=[],
                                  cache_time=None,
                                  is_personal=None,
                                  next_offset=None,
                                  switch_pm_text=None,
                                  switch_pm_parameter=None,
                                  update=None):
        """Answer inline queries.

        This method wraps lower-level `answerInlineQuery` method.
        If `results` is a string, cast it to proper type (list of dicts having
            certain keys). See utilities.make_inline_query_answer for details.
        """
        if (
            inline_query_id is None
            and isinstance(update, dict)
            and 'id' in update
        ):
            inline_query_id = update['id']
        results = make_inline_query_answer(results)
        return await self.answerInlineQuery(
            inline_query_id=inline_query_id,
            results=results,
            cache_time=cache_time,
            is_personal=is_personal,
            next_offset=next_offset,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter=switch_pm_parameter,
        )

    @classmethod
    def set_class_maintenance_message(cls, maintenance_message):
        """Set class maintenance message.

        It will be returned if bot is under maintenance, unless and instance
            `_maintenance_message` is set.
        """
        cls._maintenance_message = maintenance_message

    def set_maintenance_message(self, maintenance_message):
        """Set instance maintenance message.

        It will be returned if bot is under maintenance.
        If instance message is None, default class message is used.
        """
        self._maintenance_message = maintenance_message

    def change_maintenance_status(self, maintenance_message=None, status=None):
        """Put the bot under maintenance or end it.

        While in maintenance, bot will reply to users with maintenance_message
            with a few exceptions.
        If status is not set, it is by default the opposite of the current one.
        Optionally, `maintenance_message` may be set.
        """
        if status is None:
            status = not self.under_maintenance
        assert type(status) is bool, "status must be a boolean value!"
        self._under_maintenance = status
        if maintenance_message:
            self.set_maintenance_message(maintenance_message)
        return self._under_maintenance  # Return new status

    def is_allowed_during_maintenance(self, update):
        """Return True if update is allowed during maintenance.

        An update is allowed if any of the criteria in
            `self.allowed_during_maintenance` returns True called on it.
        """
        for criterion in self.allowed_during_maintenance:
            if criterion(update):
                return True
        return False

    def allow_during_maintenance(self, criterion):
        """Add a criterion to allow certain updates during maintenance.

        `criterion` must be a function taking a Telegram `update` dictionary
            and returning a boolean.
        ```# Example of criterion
        def allow_text_messages(update):
            if 'message' in update and 'text' in update['message']:
                return True
            return False
        ```
        """
        self._allowed_during_maintenance.append(criterion)

    async def handle_update_during_maintenance(self, update):
        """Handle an update while bot is under maintenance.

        Handle all types of updates.
        """
        if (
            'message' in update
            and 'chat' in update['message']
            and update['message']['chat']['id'] > 0
        ):
            return await self.send_message(
                text=self.maintenance_message,
                update=update['message'],
                reply_to_update=True
            )
        elif 'callback_query' in update:
            await self.answerCallbackQuery(
                callback_query_id=update['id'],
                text=remove_html_tags(self.maintenance_message[:45])
            )
        elif 'inline_query' in update:
            await self.answer_inline_query(
                update['inline_query']['id'],
                self.maintenance_message,
                cache_time=30,
                is_personal=False,
            )
        return

    @classmethod
    def set_class_authorization_denied_message(csl, message):
        """Set class authorization denied message.

        It will be returned if user is unauthorized to make a request.
        """
        csl._authorization_denied_message = message

    def set_authorization_denied_message(self, message):
        """Set instance authorization denied message.

        If instance message is None, default class message is used.
        """
        self._authorization_denied_message = message

    def set_authorization_function(self, authorization_function):
        """Set a custom authorization_function.

        It should evaluate True if user is authorized to perform a specific
            action and False otherwise.
        It should take update and role and return a Boolean.
        Default authorization_function always evaluates True.
        """
        self.authorization_function = authorization_function

    @classmethod
    def set_class_unknown_command_message(cls, unknown_command_message):
        """Set class unknown command message.

        It will be returned if user sends an unknown command in private chat.
        """
        cls._unknown_command_message = unknown_command_message

    def set_unknown_command_message(self, unknown_command_message):
        """Set instance unknown command message.

        It will be returned if user sends an unknown command in private chat.
        If instance message is None, default class message is used.
        """
        self._unknown_command_message = unknown_command_message

    def command(self, command, aliases=None, reply_keyboard_button=None,
                show_in_keyboard=False, description="",
                help_section=None,
                authorization_level='admin'):
        """Associate a bot command with a custom handler function.

        Decorate command handlers like this:
            ```
            @bot.command('/mycommand', ['Button'], True, "My command", 'user')
            async def command_handler(bot, update, user_record):
                return "Result"
            ```
        When a message text starts with `/command[@bot_name]`, or with an
            alias, it gets passed to the decorated function.
        `command` is the command name (with or without /).
        `aliases` is a list of aliases; each will call the command handler
            function; the first alias will appear as button in
            reply keyboard if `reply_keyboard_button` is not set.
        `reply_keyboard_button` is a str or better dict of language-specific
            strings to be shown in default keyboard.
        `show_in_keyboard`, if True, makes a button for this command appear in
            default keyboard.
        `description` can be used to help users understand what `/command`
            does.
        `help_section` is a dict on which the corresponding help section is
            built. It may provide multilanguage support and should be
            structured as follows:
            {
              "label": {  # It will be displayed as button label
                'en': "Label",
                ...
              },
              "name": "section_name",
              # If missing, `authorization_level` is used
              "authorization_level": "everybody",
              "description": {
                'en': "Description in English",
                ...
              },
          }
        `authorization_level` is the lowest authorization level needed to run
            the command.
        """
        if not isinstance(command, str):
            raise TypeError(f'Command `{command}` is not a string')
        if isinstance(reply_keyboard_button, dict):
            for button in reply_keyboard_button.values():
                if button not in aliases:
                    aliases.append(button)
        if aliases:
            if not isinstance(aliases, list):
                raise TypeError(f'Aliases is not a list: `{aliases}`')
            if not all(
                [
                    isinstance(alias, str)
                    for alias in aliases
                ]
            ):
                raise TypeError(
                    f'Aliases {aliases} is not a list of strings string'
                )
        if isinstance(help_section, dict):
            if 'authorization_level' not in help_section:
                help_section['authorization_level'] = authorization_level
            self.messages['help_sections'][help_section['name']] = help_section
        command = command.strip('/ ').lower()

        def command_decorator(command_handler):
            async def decorated_command_handler(bot, update, user_record):
                logging.info(
                    f"Command `{command}@{bot.name}` called by "
                    "`{from_}`".format(
                        from_=(
                            update['from']
                            if 'from' in update
                            else update['chat']
                        )
                    )
                )
                if bot.authorization_function(
                    update=update,
                    user_record=user_record,
                    authorization_level=authorization_level
                ):
                    # Pass supported arguments from locals() to command_handler
                    return await command_handler(
                        **{
                            name: argument
                            for name, argument in locals().items()
                            if name in inspect.signature(
                                command_handler
                            ).parameters
                        }
                    )
                return self.authorization_denied_message
            self.commands[command] = dict(
                handler=decorated_command_handler,
                description=description,
                authorization_level=authorization_level
            )
            if type(description) is dict:
                self.messages['commands'][command] = dict(
                    description=description
                )
            if aliases:
                for alias in aliases:
                    self.command_aliases[alias] = decorated_command_handler
            if show_in_keyboard and (aliases or reply_keyboard_button):
                _reply_keyboard_button = reply_keyboard_button or aliases[0]
                self.messages[
                    'reply_keyboard_buttons'][
                    command] = _reply_keyboard_button
                self.commands[command][
                    'reply_keyboard_button'] = _reply_keyboard_button
        return command_decorator

    def parser(self, condition, description='', authorization_level='admin',
               argument='text'):
        """Define a text message parser.

        Decorate command handlers like this:
            ```
            def custom_criteria(update):
                return 'from' in update

            @bot.parser(custom_criteria, authorization_level='user')
            async def text_parser(bot, update, user_record):
                return "Result"
            ```
        If condition evaluates True when run on a message text
            (not starting with '/'), such decorated function gets
            called on update.
        Conditions of parsers are evaluated in order; when one is True,
            others will be skipped.
        `description` provides information about the parser.
        `authorization_level` is the lowest authorization level needed to call
            the parser.
        """
        if not callable(condition):
            raise TypeError(
                f'Condition {condition.__name__} is not a callable'
            )

        def parser_decorator(parser):
            async def decorated_parser(bot, update, user_record):
                logging.info(
                    f"Text message update matching condition "
                    f"`{condition.__name__}@{bot.name}` from "
                    "`{user}`".format(
                        user=(
                            update['from']
                            if 'from' in update
                            else update['chat']
                        )
                    )
                )
                if bot.authorization_function(
                    update=update,
                    user_record=user_record,
                    authorization_level=authorization_level
                ):
                    # Pass supported arguments from locals() to parser
                    return await parser(
                        **{
                            name: argument
                            for name, argument in locals().items()
                            if name in inspect.signature(parser).parameters
                        }
                    )
                return bot.authorization_denied_message
            self.text_message_parsers[condition] = dict(
                handler=decorated_parser,
                description=description,
                authorization_level=authorization_level,
                argument=argument
            )
        return parser_decorator

    def set_command(self, command, handler, aliases=None,
                    reply_keyboard_button=None, show_in_keyboard=False,
                    description="",
                    authorization_level='admin'):
        """Associate a `command` with a `handler`.

        When a message text starts with `/command[@bot_name]`, or with an
            alias, it gets passed to the decorated function.
        `command` is the command name (with or without /)
        `handler` is the function to be called on update objects.
        `aliases` is a list of aliases; each will call the command handler
            function; the first alias will appear as button in
            reply keyboard if `reply_keyboard_button` is not set.
        `reply_keyboard_button` is a str or better dict of language-specific
            strings to be shown in default keyboard.
        `show_in_keyboard`, if True, makes a button for this command appear in
            default keyboard.
        `description` is a description and can be used to help users understand
            what `/command` does.
        `authorization_level` is the lowest authorization level needed to run
            the command.
        """
        if not callable(handler):
            raise TypeError(f'Handler `{handler}` is not callable.')
        return self.command(
            command=command, aliases=aliases,
            reply_keyboard_button=reply_keyboard_button,
            show_in_keyboard=show_in_keyboard, description=description,
            authorization_level=authorization_level
        )(handler)

    def button(self, prefix, separator=None, description='',
               authorization_level='admin'):
        """Associate a bot button `prefix` with a handler.

        When a callback data text starts with `prefix`, the associated handler
            is called upon the update.
        Decorate button handlers like this:
            ```
            @bot.button('a_prefix:///', description="A button",
                        authorization_level='user')
            async def button_handler(bot, update, user_record, data):
                return "Result"
            ```
        `separator` will be used to parse callback data received when a button
            starting with `prefix` will be pressed.
        `description` contains information about the button.
        `authorization_level` is the lowest authorization level needed to
            be allowed to push the button.
        """
        if not isinstance(prefix, str):
            raise TypeError(
                f'Inline button callback_data {prefix} is not a string'
            )

        def button_decorator(handler):
            async def decorated_button_handler(bot, update, user_record):
                logging.info(
                    f"Button `{update['data']}`@{bot.name} pressed by "
                    f"`{update['from']}`"
                )
                if bot.authorization_function(
                    update=update,
                    user_record=user_record,
                    authorization_level=authorization_level
                ):
                    # Remove `prefix` from `data`
                    data = extract(update['data'], prefix)
                    # If a specific separator or default separator is set,
                    #   use it to split `data` string in a list.
                    #   Cast numeric `data` elements to `int`.
                    _separator = separator or self.callback_data_separator
                    if _separator:
                        data = [
                            int(element) if element.isnumeric()
                            else element
                            for element in data.split(_separator)
                        ]
                    # Pass supported arguments from locals() to handler
                    return await handler(
                        **{
                            name: argument
                            for name, argument in locals().items()
                            if name in inspect.signature(handler).parameters
                        }
                    )
                return bot.authorization_denied_message
            self.callback_handlers[prefix] = dict(
                handler=decorated_button_handler,
                description=description,
                authorization_level=authorization_level
            )
        return button_decorator

    def query(self, condition, description='', authorization_level='admin'):
        """Define an inline query.

        Decorator: `@bot.query(example)`
        When an inline query matches the `condition` function,
            decorated function is called and passed the query update object
            as argument.
        `description` is a description
        `authorization_level` is the lowest authorization level needed to run
            the command
        """
        if not callable(condition):
            raise TypeError(
                'Condition {c} is not a callable'.format(
                    c=condition.__name__
                )
            )

        def query_decorator(handler):
            async def decorated_query_handler(bot, update, user_record):
                logging.info(
                    f"Inline query matching condition "
                    f"`{condition.__name__}@{bot.name}` from "
                    f"`{update['from']}`"
                )
                if self.authorization_function(
                    update=update,
                    user_record=user_record,
                    authorization_level=authorization_level
                ):
                    # Pass supported arguments from locals() to handler
                    return await handler(
                        **{
                            name: argument
                            for name, argument in locals().items()
                            if name in inspect.signature(handler).parameters
                        }
                    )
                return self.authorization_denied_message
            self.inline_query_handlers[condition] = dict(
                handler=decorated_query_handler,
                description=description,
                authorization_level=authorization_level
            )
        return query_decorator

    def set_chat_id_getter(self, getter):
        """Set chat_id getter.

        It must be a function that takes an update and returns the proper
            chat_id.
        """
        assert callable(getter), "Chat id getter must be a function!"
        self.get_chat_id = getter

    @staticmethod
    def get_user_identifier(user_id=None, update=None):
        """Get telegram id of user given an update.

        Result itself may be passed as either parameter (for backward
            compatibility).
        """
        identifier = user_id or update
        assert identifier is not None, (
            "Provide a user_id or update object to get a user identifier."
        )
        if (
            isinstance(identifier, dict)
            and 'message' in identifier
            and 'from' not in identifier
        ):
            identifier = identifier['message']
        if isinstance(identifier, dict) and 'from' in identifier:
            identifier = identifier['from']['id']
        assert type(identifier) is int, (
            f"Unable to find a user identifier. Got `{identifier}`"
        )
        return identifier

    @staticmethod
    def get_message_identifier(update=dict()):
        """Get a message identifier dictionary to edit `update`.

        Pass the result as keyword arguments to `edit...` API methods.
        """
        if 'message' in update:
            update = update['message']
        if 'chat' in update and 'message_id' in update:
            return dict(
                chat_id=update['chat']['id'],
                message_id=update['message_id']
            )
        elif 'inline_message_id' in update:
            return dict(
                inline_message_id=update['inline_message_id']
            )

    def set_individual_text_message_handler(self, handler,
                                            update=None, user_id=None):
        """Set a custom text message handler for the user.

        Any text message update from the user will be handled by this custom
            handler instead of default handlers for commands, aliases and text.
        Custom handlers last one single use, but they can call this method and
            set themselves as next custom text message handler.
        """
        identifier = self.get_user_identifier(
            user_id=user_id,
            update=update
        )
        assert callable(handler), (f"Handler `{handler.name}` is not "
                                   "callable. Custom text message handler "
                                   "could not be set.")
        self.individual_text_message_handlers[identifier] = handler
        return

    def remove_individual_text_message_handler(self,
                                               update=None, user_id=None):
        """Remove a custom text message handler for the user.

        Any text message update from the user will be handled by default
            handlers for commands, aliases and text.
        """
        identifier = self.get_user_identifier(
            user_id=user_id,
            update=update
        )
        if identifier in self.individual_text_message_handlers:
            del self.individual_text_message_handlers[identifier]
        return

    def set_individual_location_handler(self, handler,
                                        update=None, user_id=None):
        """Set a custom location handler for the user.

        Any location update from the user will be handled by this custom
            handler instead of default handlers for commands, aliases and text.
        Custom handlers last one single use, but they can call this method and
            set themselves as next custom handler.
        """
        identifier = self.get_user_identifier(
            user_id=user_id,
            update=update
        )
        assert callable(handler), (f"Handler `{handler.name}` is not "
                                   "callable. Custom location handler "
                                   "could not be set.")
        self.individual_location_handlers[identifier] = handler
        return

    def remove_individual_location_handler(self,
                                           update=None, user_id=None):
        """Remove a custom location handler for the user.

        Any location message update from the user will be handled by default
            handlers for commands, aliases and text.
        """
        identifier = self.get_user_identifier(
            user_id=user_id,
            update=update
        )
        if identifier in self.individual_location_handlers:
            del self.individual_location_handlers[identifier]
        return

    async def webhook_feeder(self, request):
        """Handle incoming HTTP `request`s.

        Get data, feed webhook and return and OK message.
        """
        update = await request.json()
        asyncio.ensure_future(
            self.route_update(update)
        )
        return web.Response(
            body='OK'.encode('utf-8')
        )

    async def get_me(self):
        """Get bot information.

        Restart bots if bot can't be got.
        """
        try:
            me = await self.getMe()
            if isinstance(me, Exception):
                raise me
            elif me is None:
                raise Exception('getMe returned None')
            self._name = me["username"]
            self._telegram_id = me['id']
        except Exception as e:
            logging.error(
                f"API getMe method failed, information about this bot could "
                f"not be retrieved. Restarting in 5 minutes...\n\n"
                f"Error information:\n{e}"
            )
            await asyncio.sleep(5*60)
            self.__class__.stop(
                65,
                "Information about this bot could not be retrieved.\n"
                "Restarting..."
            )

    def setup(self):
        """Make bot ask for updates and handle responses."""
        if not self.webhook_url:
            asyncio.ensure_future(self.get_updates())
        else:
            asyncio.ensure_future(self.set_webhook())
            self.__class__.app.router.add_route(
                'POST', self.webhook_local_address, self.webhook_feeder
            )
        asyncio.ensure_future(self.update_users())

    async def close_sessions(self):
        """Close open sessions."""
        for session_name, session in self.sessions.items():
            if not session.closed:
                await session.close()

    async def set_webhook(self, url=None, certificate=None,
                          max_connections=None, allowed_updates=None):
        """Set a webhook if token is valid."""
        # Return if token is invalid
        await self.get_me()
        if self.name is None:
            return
        webhook_was_set = await self.setWebhook(
            url=url, certificate=certificate, max_connections=max_connections,
            allowed_updates=allowed_updates
        )  # `setWebhook` API method returns `True` on success
        webhook_information = await self.getWebhookInfo()
        webhook_information['url'] = webhook_information['url'].replace(
            self.token, "<BOT_TOKEN>"
        ).replace(
            self.session_token, "<SESSION_TOKEN>"
        )
        if webhook_was_set:
            logging.info(
                f"Webhook was set correctly.\n"
                f"Webhook information: {webhook_information}"
            )
        else:
            logging.error(
                f"Failed to set webhook!\n"
                f"Webhook information: {webhook_information}"
            )

    async def get_updates(self, timeout=30, limit=100, allowed_updates=None,
                          error_cooldown=10):
        """Get updates using long polling.

        timeout : int
            Timeout set for Telegram servers. Make sure that connection timeout
            is greater than `timeout`.
        limit : int (1 - 100)
            Max number of updates to be retrieved.
        allowed_updates : List(str)
            List of update types to be retrieved.
            Empty list to allow all updates.
            None to fallback to class default.
        """
        # Return if token is invalid
        await self.get_me()
        if self.name is None:
            return
        # Set custom list of allowed updates or fallback to class default list
        if allowed_updates is None:
            allowed_updates = self.allowed_updates
        await self.deleteWebhook()  # Remove eventually active webhook
        update = None  # Do not update offset if no update is received
        while True:
            updates = await self.getUpdates(
                offset=self._offset,
                timeout=timeout,
                limit=limit,
                allowed_updates=allowed_updates
            )
            if updates is None:
                continue
            elif isinstance(updates, TelegramError):
                logging.error(
                    f"Waiting {error_cooldown} seconds before trying again..."
                )
                await asyncio.sleep(error_cooldown)
                continue
            elif isinstance(updates, Exception):
                logging.error(
                    "Unexpected exception. "
                    f"Waiting {error_cooldown} seconds before trying again..."
                )
                await asyncio.sleep(error_cooldown)
                continue
            for update in updates:
                asyncio.ensure_future(self.route_update(update))
            if update is not None:
                self._offset = update['update_id'] + 1

    async def update_users(self, interval=60):
        """Every `interval` seconds, store news about bot users.

        Compare `update['from']` data with records in `users` table and keep
            track of differences in `users_history` table.
        """
        while 1:
            await asyncio.sleep(interval)
            # Iterate through a copy since asyncio.sleep(0) is awaited at each
            # cycle iteration.
            for telegram_id, user in self.recent_users.copy().items():
                new_record = dict()
                with self.db as db:
                    user_record = db['users'].find_one(telegram_id=telegram_id)
                    for key in [
                        'first_name',
                        'last_name',
                        'username',
                        'language_code'
                    ]:
                        new_record[key] = (user[key] if key in user else None)
                        if (
                            (
                                key not in user_record
                                or new_record[key] != user_record[key]
                            )
                            # Exclude fake updates
                            and 'notes' not in user
                        ):
                            db['users_history'].insert(
                                dict(
                                    until=datetime.datetime.now(),
                                    user_id=user_record['id'],
                                    field=key,
                                    value=(
                                        user_record[key]
                                        if key in user_record
                                        else None
                                    )
                                )
                            )
                            db['users'].update(
                                {
                                    'id': user_record['id'],
                                    key: new_record[key]
                                },
                                ['id'],
                                ensure=True
                            )
                if telegram_id in self.recent_users:
                    del self.recent_users[telegram_id]
                await asyncio.sleep(0)

    def get_user_record(self, update):
        """Get user_record of update sender.

        If user is unknown add them.
        If update has no `from` field, return None.
        If user data changed, ensure that this event gets stored.
        """
        if 'from' not in update or 'id' not in update['from']:
            return
        telegram_id = update['from']['id']
        with self.db as db:
            user_record = db['users'].find_one(
                telegram_id=telegram_id
            )
            if user_record is None:
                new_user = dict(
                    telegram_id=telegram_id,
                    privileges=100,
                    selected_language_code=None
                )
                for key in [
                    'first_name',
                    'last_name',
                    'username',
                    'language_code'
                ]:
                    new_user[key] = (
                        update['from'][key]
                        if key in update['from']
                        else None
                    )
                db['users'].insert(new_user)
                user_record = db['users'].find_one(
                    telegram_id=telegram_id
                )
            elif (
                telegram_id not in self.recent_users
                and 'notes' not in update['from']  # Exclude fake updates
            ):
                self.recent_users[telegram_id] = update['from']
        return user_record

    def set_router(self, event, handler):
        """Set `handler` as router for `event`."""
        self.routing_table[event] = handler

    async def route_update(self, update):
        """Pass `update` to proper method.

        Update objects have two keys:
        - `update_id` (which is used as offset while retrieving new updates)
        - One and only one of the following
            `message`
            `edited_message`
            `channel_post`
            `edited_channel_post`
            `inline_query`
            `chosen_inline_result`
            `callback_query`
            `shipping_query`
            `pre_checkout_query`
            `poll`
        """
        if (
            self.under_maintenance
            and not self.is_allowed_during_maintenance(update)
        ):
            return await self.handle_update_during_maintenance(update)
        for key, value in update.items():
            if key in self.routing_table:
                user_record = self.get_user_record(update=value)
                return await self.routing_table[key](
                    update=value,
                    user_record=user_record
                )
        logging.error(f"Unknown type of update.\n{update}")

    def additional_task(self, when='BEFORE', *args, **kwargs):
        """Add a task before at app start or cleanup.

        Decorate an async function to have it awaited `BEFORE` or `AFTER` main
            loop.
        """
        when = when[0].lower()

        def additional_task_decorator(task):
            if when == 'b':
                self.preliminary_tasks.append(task(*args, **kwargs))
            elif when == 'a':
                self.final_tasks.append(task(*args, **kwargs))
        return additional_task_decorator

    @classmethod
    async def start_app(cls):
        """Start running `aiohttp.web.Application`.

        It will route webhook-received updates and other custom paths.
        """
        assert cls.local_host is not None, "Invalid local host"
        assert cls.port is not None, "Invalid port"
        cls.runner = web.AppRunner(cls.app)
        await cls.runner.setup()
        cls.server = web.TCPSite(cls.runner, cls.local_host, cls.port)
        try:
            await cls.server.start()
        except OSError as e:
            logging.error(e)
            raise KeyboardInterrupt("Unable to start web app.")
        logging.info(f"App running at http://{cls.local_host}:{cls.port}")

    @classmethod
    async def stop_app(cls):
        """Close bot sessions and cleanup."""
        for bot in cls.bots:
            await asyncio.gather(
                *bot.final_tasks
            )
            await bot.close_sessions()
        await cls.runner.cleanup()

    @classmethod
    def stop(cls, message, final_state=0):
        """Log a final `message`, stop loop and set exiting `code`.

        All bots and the web app will be terminated gracefully.
        The final state may be retrieved to get information about what stopped
            the bots.
        """
        logging.info(message)
        cls.final_state = final_state
        cls.loop.stop()
        return

    @classmethod
    def run(cls, local_host=None, port=None):
        """Run aiohttp web app and all Bot instances.

        Each bot will receive updates via long polling or webhook according to
            its initialization parameters.
        A single aiohttp.web.Application instance will be run (cls.app) on
            local_host:port and it may serve custom-defined routes as well.
        """
        if local_host is not None:
            cls.local_host = local_host
        if port is not None:
            cls.port = port
        try:
            cls.loop.run_until_complete(
                asyncio.gather(
                    *[
                        preliminary_task
                        for bot in cls.bots
                        for preliminary_task in bot.preliminary_tasks
                    ]
                )
            )
        except Exception as e:
            logging.error(f"{e}", exc_info=True)
        for bot in cls.bots:
            bot.setup()
        asyncio.ensure_future(cls.start_app())
        try:
            cls.loop.run_forever()
        except KeyboardInterrupt:
            logging.info("Stopped by KeyboardInterrupt")
        except Exception as e:
            logging.error(f"{e}", exc_info=True)
        finally:
            cls.loop.run_until_complete(cls.stop_app())
        return cls.final_state
