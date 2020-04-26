from datetime import datetime
from threading import Thread

from lib import CTDT, Config, Cache
import time
from tsubasa import Tsubasa
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Update, Message

DEBUG = False

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CTDT.initialize()
config: Config = Config.get_instance()
caches: Cache = Cache.get_instance()
CTDT.convert_templates_to_jpeg()
CTDT.initialize_cache()

# telegram bot updater
updater: Updater = None
thread_telegram = None
thread_ctdt = None

print("Start Processing : {0}".format(datetime.now()))


####################################################################


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def telegram_start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def telegram_help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def telegram_msg(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def telegram_error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def telegram_screenshot(update: Update, context):
    CTDT.save_screenshot()
    msg: Message = update.message
    msg.reply_photo(open("screenshot.jpg", "rb"))


####################################################################

def telegram_bot():
    global updater

    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(config.telegram_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", telegram_start))
    dp.add_handler(CommandHandler("help", telegram_help))
    dp.add_handler(CommandHandler("screenshot", telegram_screenshot))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, telegram_msg))

    # log all errors
    dp.add_error_handler(telegram_error)

    # Start the Bot
    updater.start_polling()


def ctdt():
    tsubasa: Tsubasa = Tsubasa()

    while True:

        if DEBUG:
            result = tsubasa.run()
            print(result)
            time.sleep(config.sleep)
        else:
            try:
                result = tsubasa.run()
                time.sleep(config.sleep)
            except Exception as ex:
                print(str(ex))


if config.telegram_disabled == 0:
    thread_telegram = Thread(target=telegram_bot)
thread_ctdt = Thread(target=ctdt)

if __name__ == "__main__":
    # execute only if run as a script

    thread_ctdt.start()

    if config.telegram_disabled == 0:
        thread_telegram.start()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()

    thread_ctdt.join()
    if config.telegram_disabled == 0:
        thread_telegram.join()
