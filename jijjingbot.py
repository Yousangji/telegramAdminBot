import logging

from telegram import KeyboardButton, ParseMode, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from Model import menu

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def group_messagehandler(bot, update):
    """get message not mentioned and buttons response."""

    '''check if is button response'''
    message_text = update.message.text
    if message_text in [*menu]:
        response = menu[message_text]
        bot.sendMessage(update.message.chat.id, text=response, reply_to_message_id=update.message.message_id,
                        parse_mode=ParseMode.MARKDOWN)
    else:
        pass


def requestQuestion(bot, update):
    '''F&Q selective keyboard
    1. mention bot
      1.1 send keyboard'''
    message = update.message
    entities = message.parse_entities()

    if '@JijjingBot' in entities.values():
        keyboards = [[KeyboardButton(s)] for s in [*menu]]
        reply_markup2 = ReplyKeyboardMarkup(keyboards, one_time_keyboard=True, selective=True, resize_keyboard=True)
        username = f"[{update.message.from_user.first_name}](tg://user?id={update.message.from_user.id})"
        bot.sendMessage(chat_id=message.chat.id,
                        text=f"{username} 님 무엇을 도와드릴까요? :)",
                        reply_markup=reply_markup2, parse_mode=ParseMode.MARKDOWN)
    else:
        pass


def welcome(bot, update):
    usernameMention = f"[{update.message.from_user.first_name}](tg://user?id={update.message.from_user.id})"
    text = f' {usernameMention}님 안녕하세요! 반갑습니다~😊 '
    keyboards = [[KeyboardButton(s)] for s in [*menu]]
    reply_markup2 = ReplyKeyboardMarkup(keyboards, one_time_keyboard=True, selective=True, resize_keyboard=True)
    bot.sendMessage(chat_id=update.message.chat.id, text=text, parse_mode=ParseMode.MARKDOWN,reply_markup=reply_markup2)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    token = "586197556:AAF0NxAf5RfZjEV123miMnUxPS0B2Hd6gSY"
    updater = Updater(token=token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.entity(entity_type="mention"), requestQuestion))
    dp.add_handler(MessageHandler(Filters.text and Filters.group, callback=group_messagehandler))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
