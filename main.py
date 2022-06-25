import time

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update, InlineKeyboardButton, \
    InlineKeyboardMarkup
from random import randint
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, ConversationHandler
from telegram.ext import MessageHandler, Filters, InlineQueryHandler
import token_XO
from time import sleep

GAME_CYCLE, RESULT = range(2)
flag = 1
candy = 2021
TOKEN = token_XO.TOKEN
updater = Updater(token=token_XO.TOKEN)
dispatcher = updater.dispatcher


# функция обработки команды '/start' Стандартная функция которая шла в изначальном файле
def start(update, context: CallbackContext):
    update.message.from_user.first_name
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Привет, <b>{update.message.from_user.first_name}</b> \U0001F609, предлагаю "
                                  f"тебе сыграть в игру.\n"
                                  "\nПравила очень просты: на столе лежит <b>2021 конфета</b>.\n"
                                  "Играем ты да я, делая ход друг после друга.\n"
                                  "Первый ход определяется жеребьевкой. \n"
                                  "<i>За один ход</i> можно забрать <i>не более</i> чем <b>28 конфет</b>.\n"
                                  "Все конфеты оппонента <s>а также диатез</s> достаются \nсделавшему"
                                  " последний ход.\n "
                                  "\nПопробуй обыграй меня \U0001F608"
                                  "\n/play | /exit", parse_mode='html')
    return GAME_CYCLE


def exit_func(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"<b>{update.message.from_user.first_name}</b>, уже уходишь? "
                                  f"Тебе не понравилась игра\U0001F97A? В любом случае ты всегда можешь вернуться"
                                  f"и попробовать сыграть еще. \nДо свидания \U0001F64B \U0001F64B\u200D\u2642\uFE0F "
                                  f"", parse_mode='html')


def play(update, context):
    context.bot.send_animation(chat_id=update.effective_chat.id,
                               animation='https://media.giphy.com/media/ckHAdLU2OmY7knUClD/giphy.gif')

    def turn():
        whos_turn = randint(1, 6)
        if whos_turn % 2 == 0:
            message = 'Жеребьевка проведена, вы выбираете первым...'
        else:
            message = 'Жеребьевка проведена, я выбираю первым...'
        return message

    message = turn()
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f'{message}')
    return GAME_CYCLE


def game_cycle(update, context, turn):
    global flag

    def player_start():
        global candy, flag
        print(update.message.text)
        candy -= int(update.message.text)
        take_candy = randint(1, 28)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'Выбирайте сколько возьмете конфет. Напишите число от 1 до 28')
        flag = 1
        return GAME_CYCLE

    def bot_start():
        global candy, flag
        take_candy = randint(1, 28)
        candy -= take_candy
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'Я беру {take_candy} конфет. Конфет осталось {candy}')
        flag = 0
        return GAME_CYCLE

    if flag == 1:
        bot_start()
    else:
        player_start()
    return GAME_CYCLE


def result(update, context):
    global flag
    if flag == 1:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'Поздравляю вас с победой!')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'К сожалению, вы проиграли, может повезет в следующий раз?')


def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Тебе нужна помощь?\U0001F914 \n\n"
                                  "Смотри, на самом деле правила просты."
                                  " Всего есть <b>2021 конфета</b>. \nИграют <b>2 человека</b>."
                                  "Чтобы определить кто ходит первый можно, например, подкинуть монетку. "
                                  "За <i>один</i> ход можно взять не более чем <b>28 конфет</b>, но при этом "
                                  "держи в голове, "
                                  "что не обязательно брать по максимуму или по минимуму. Не спеши, думай как "
                                  "обыграть меня "
                                  "и внимательно следи за количеством конфет. Твоя задача подгадать так "
                                  "чтобы забрать последние конфеты и тогда победа \U0001F973 будет за тобой!"
                                  "\nУдачи!\u263A\uFE0F \n\n"
                                  "/start | /play | /exit |", parse_mode='html')


# функция обработки не распознных команд
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Неверная команда!\n"
                                  "\nСписок команд:\n"
                                  "/start | /play | /exit | /help")


# обработчик команды '/start'
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# обработчик game
play_handler = CommandHandler('play', play)
dispatcher.add_handler(play_handler)

# обработчик help
help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

# exit_func_handler = CommandHandler('exit', exit_func)
# dispatcher.add_handler(exit_func_handler)

conv_handler = ConversationHandler(  # здесь строится логика разговора
    # точка входа в разговор
    entry_points=[CommandHandler('start', start)],
    # этапы разговора, каждый со своим списком обработчиков сообщений
    states={
        GAME_CYCLE: [MessageHandler(Filters.text, game_cycle)],# if candy > 0 else result
        RESULT: [MessageHandler(Filters.text & ~Filters.command, result)],
    },
    # точка выхода из разговора
    fallbacks=[CommandHandler('exit', exit_func)],
)

# Добавляем обработчик разговоров `conv_handler`
dispatcher.add_handler(conv_handler)

# обработчик не распознанных команд. Должен быть обязательно в конце чтобы не перехватывать команды которые идут раньше
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

# запуск прослушивания сообщений
updater.start_polling()
# обработчик нажатия Ctrl+C
updater.idle()
