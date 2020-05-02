import os
import sys
from datetime import datetime

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from lib import CTDT, Config
from telegram import Update, Message
import logging
from telegram import Bot


class TelegramBot:
    # telegram bot updater
    updater: Updater = None
    logger = None

    # telegral bot
    bot: Bot

    config: Config

    # pause loop
    pause_flag = False

    # flag that indicate we want a graceful exit of app
    exit_app_flag = False

    # flag that indicate we need and urgent exit of app
    force_exit_app_flag = False

    # go home flag
    go_home_flag = False

    def __init__(self):
        self.config = Config.get_instance()

        # do not start bot if it is disabled in config
        if self.config.telegram_disabled == 1: return

        # inform boss we are starting
        self.bot = Bot(token=self.config.telegram_token)
        msg1 = "Starting bot: {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.bot.send_message(self.config.telegram_chatid, msg1)
        self.bot.send_message(self.config.telegram_chatid, self.config.get_text_mode())
        self.bot.send_message(self.config.telegram_chatid, self.config.get_text_difficulty())

        msg2 = "Mode : "

        # Enable logging
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

        self.logger = logging.getLogger(__name__)

        """Start the bot."""
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        updater = Updater(self.config.telegram_token, use_context=True)

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # on screenshot command
        dp.add_handler(CommandHandler("screenshot", self.screenshot))

        # on restart command
        dp.add_handler(CommandHandler("restart", self.restart))

        # on setmode command
        dp.add_handler(CommandHandler("setmode", self.set_mode))

        # on pause command
        dp.add_handler(CommandHandler("pause", self.pause))

        # on resume command
        dp.add_handler(CommandHandler("resume", self.resume))

        # on exit command
        dp.add_handler(CommandHandler("exit", self.exit))

        # on force exit command
        dp.add_handler(CommandHandler("forceexit", self.force_exit))

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

    def restart(self, update: Update, context):
        output: str = "Restarting bot : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        msg: Message = update.message
        msg.reply_text(output)
        sys.argv.append("-r")
        os.execl(sys.executable, sys.argv[0], *sys.argv)

    def set_mode(self, update: Update, context):
        try:
            msg: Message = update.message
            text = msg.text.split()[1]
            mode = int(text)
            self.config.mode = mode

            msg2 = self.config.get_text_mode()

            self.bot.send_message(self.config.telegram_chatid, msg2)
        except Exception as ex:
            print(str(ex))
            self.bot.send_message(self.config.telegram_chatid, "SetMode : Error")

    def pause(self, update: Update, context):
        self.pause_flag = True
        output: str = "Pause : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        msg: Message = update.message
        msg.reply_text(output)

    def resume(self, update: Update, context):
        self.pause_flag = False
        output: str = "Resume : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        msg: Message = update.message
        msg.reply_text(output)

    def exit(self, update: Update, context):
        self.exit_app_flag = True
        output: str = "Star exiting : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        msg: Message = update.message
        msg.reply_text(output)

    def force_exit(self, update: Update, context):
        self.force_exit_app_flag = True
        output: str = "Start forcing exit : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        msg: Message = update.message
        msg.reply_text(output)

    def home(self, update: Update, context):
        self.go_home_flag = True
        output: str = "Start going home : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        msg: Message = update.message
        msg.reply_text(output)

    def reset_go_home_flag(self):
        self.go_home_flag = False
        self.pause_flag = True
        output: str = "End going home : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.bot.send_message(self.config.telegram_chatid, output)

        output2: str = "Pause : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.bot.send_message(self.config.telegram_chatid, output2)

    def reset_exit_app(self):
        self.exit_app_flag = False
        self.pause_flag = True
        output: str = "End exit : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.bot.send_message(self.config.telegram_chatid, output)

        output2: str = "Pause : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.bot.send_message(self.config.telegram_chatid, output2)

    def reset_force_exit_app(self):
        self.force_exit_app_flag = False
        self.pause_flag = True
        output: str = "End force exit : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.bot.send_message(self.config.telegram_chatid, output)

        output2: str = "Pause : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.bot.send_message(self.config.telegram_chatid, output2)
