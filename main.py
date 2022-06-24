from telegram import InlineQueryResultArticle, InputTextMessageContent, Update, InlineKeyboardButton, \
    InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram.ext import MessageHandler, Filters, InlineQueryHandler

import token_XO

TOKEN = token_XO.TOKEN
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


# функция обработки команды '/start' Стандартная функция которая шла в изначальном файле
def start(update: Update, context: CallbackContext):
    update.message.from_user.first_name
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Привет, <b>{update.message.from_user.first_name}</b>, предлагаю тебе сыграть в игру.\n"
                                  "\nПравила очень просты: на столе лежит <b>2021 конфета</b>.\n"
                                  "Играем мы с тобой, делая ход друг после друга.\n"
                                  "Первый ход определяется жеребьевкой. \n"
                                  "<i>За один ход</i> можно забрать <i>не более чем 28 конфет</i>.\n"
                                  "Все конфеты оппонента <s>а также диатез</s> достаются \nсделавшему"
                                  " последний ход.\n "
                                  "\nПопробуй обыграй меня :)"
                                  "\n/play | /exit", parse_mode='html')





def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    #Печатает вообще всё что есть в запросе. Типа {'id': '1958782206708530086', 'message': {'text': 'Please choose:',
    print(query, '\n', query.data)

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text=f"Selected option: {query.data}")

# функция обработки текстовых сообщений
def echo(update, context):
    if update.message.text != 'help':
        text = 'ECHO: ' + update.message.text
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=text)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Вам нужна помощь?')


# функция обработки команды '/caps'
def caps(update, context):
    if context.args:
        text_caps = ' '.join(context.args).upper()
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=text_caps)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='No command argument')
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='send: /caps argument')

# функция обработки встроенного запроса
def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Convert to UPPER TEXT',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)

# функция обработки не распознных команд
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry, I didn't understand that command.")

# обработчик команды '/start'
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# обработчик текстовых сообщений
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

# обработчик команды '/caps'
caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

# обработчик встроенных запросов
inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)

# Обрабатываем нажатие кнопки
updater.dispatcher.add_handler(CallbackQueryHandler(button))

# обработчик не распознанных команд. Должен быть обязательно в конце чтобы не перехватывать команды которые идут раньше
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

# запуск прослушивания сообщений
updater.start_polling()
# обработчик нажатия Ctrl+C
updater.idle()