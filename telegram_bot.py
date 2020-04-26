from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from lib import CTDT, Config
from telegram import Update, Message
import logging


class TelegramBot:
    # telegram bot updater
    updater: Updater = None
    logger = None

    def __init__(self, token: str, disabled: int = 0):
        # do not start bot if it is disabled in config
        if disabled == 1: return

        # Enable logging
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

        self.logger = logging.getLogger(__name__)

        """Start the bot."""
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        updater = Updater(token, use_context=True)

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # on different commands - answer in Telegram
        dp.add_handler(CommandHandler("screenshot", self.screenshot))

        # log all errors
        dp.add_error_handler(self.error)

        # Start the Bot
        updater.start_polling(poll_interval=1, clean=True)

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        # self.updater.idle()

    def error(self, update, context):
        """Log Errors caused by Updates."""
        self.logger.warning('Update "%s" caused error "%s"', update, context.error)

    def screenshot(self, update: Update, context):
        CTDT.save_screenshot()
        msg: Message = update.message
        msg.reply_photo(open("screenshot.jpg", "rb"))
