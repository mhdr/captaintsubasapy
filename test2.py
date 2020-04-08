from telegram import Bot
from datetime import datetime

bot = Bot(token="696795152:AAFc1_UzsLyo2SA_By39EwH5PqiwXfZ6X8o")

bot.send_message(86168181, "Date : {0}".format(datetime.now()))
