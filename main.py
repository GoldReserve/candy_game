from random import randint
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater, CommandHandler, ConversationHandler
import token_XO


GAME_CYCLE, PLAY, RESULT = range(3)
# Чья очередь ходить
flag = 1
candy = 2021
TOKEN = token_XO.TOKEN
updater = Updater(token=token_XO.TOKEN)
dispatcher = updater.dispatcher


def start(update, _):
    global candy
    candy = 2021
    update.message.reply_text(
        text=f"Привет, <b>{update.message.from_user.first_name}</b> \U0001F609, предлагаю "
             f"тебе сыграть в игру.\n"
             "\nПравила очень просты: на столе лежит <b>2021 конфета</b>.\n"
             "Играем ты да я, делая ход друг после друга.\n"
             "Первый ход определяется жеребьевкой. \n"
             "<i>За один ход</i> можно забрать <i>не более</i> чем <b>28 конфет</b>.\n"
             "Все конфеты оппонента <s>а также диатез</s> достаются \nсделавшему"
             " последний ход.\n "
             "\nПопробуй обыграй меня \U0001F608"
             "\n/play | /exit | /help", parse_mode='html')
    return PLAY


def exit_func(update, _):
    update.message.reply_text(
        text=f"<b>{update.message.from_user.first_name}</b>, уже уходишь? "
             f"Тебе не понравилась игра\U0001F97A? В любом случае ты всегда можешь вернуться"
             f"и попробовать сыграть еще. \nДо свидания \U0001F64B \U0001F64B\u200D\u2642\uFE0F "
             f"", parse_mode='html')
    return ConversationHandler.END


def play(update, _):
    update.message.reply_animation(
        animation='https://media.giphy.com/media/ckHAdLU2OmY7knUClD/giphy.gif')

    def turn():
        global flag
        whos_turn = randint(1, 6)
        if whos_turn % 2 == 0:
            message = 'Жеребьевка проведена, вы выбираете первым...'
            flag = 1
        else:
            message = 'Жеребьевка проведена, я выбираю первым...'
            flag = 0
        return message
    message = turn()
    update.message.reply_text(text=f'{message}')
    update.message.reply_text(
        text='Нажмите /ok чтобы продолжить' if message == 'Жеребьевка проведена, я выбираю первым...'
        else f'Выбирайте сколько возьмете конфет. Напишите число от 1 до 28')
    return GAME_CYCLE


def game_cycle1(update, _):
    global flag, candy

    def player_start():
        global candy, flag
        # Сделал опции при ответе, но хорошо бы докрутить
        message1 = 'Решил взять поменьше? Понимаю...'
        # message2 = 'Решил взять средне? Хороший выбор...'
        message3 = 'Решил взять побольше? Интересно..'
        candy -= int(update.message.text)
        update.message.reply_text(text=f'Значит {update.message.text} ? {message1 if candy < 15 else message3}')
        update.message.reply_text(text=f'Нажмите /ok чтобы продолжить')
        flag = 0
        return GAME_CYCLE if candy > 0 else RESULT

    def bot_start():
        global candy, flag
        if candy > 28:
            take_candy = randint(1, 28)
        else:
            take_candy = candy - 1
        candy -= take_candy
        update.message.reply_text(text=f'Я беру {take_candy} конфет. Конфет осталось {candy}')
        update.message.reply_text(text=f'Выбирайте сколько возьмете конфет. Напишите число от 1 до 28')

        flag = 1
        return GAME_CYCLE if candy > 0 else RESULT

    if flag == 0:
        bot_start()
    else:
        player_start()
    return RESULT if candy < 1 else GAME_CYCLE


def result(update, _):
    global flag
    if flag == 0:
        update.message.reply_text(
            text=f'Поздравляю вас с победой!')
        update.message.reply_animation(
            animation='https://media0.giphy.com/media/BgDhQlomMxRPq/giphy.gif?cid=ecf05e'
                      '47k6vvsufku78qr4otj2kjyzs9t3l3g8zz5w2zu1vw&rid=giphy.gif&ct=g')
    else:
        update.message.reply_text(
            text=f'К сожалению, вы проиграли, может повезет в следующий раз?')
        update.message.reply_animation(
            animation='https://media4.giphy.com/media/RHEGP4TpkhrQTFCZE4/giphy.gif?'
                      'cid=ecf05e47j1h7ru1st6wzu09ooj2f7f442zt1elrsmcfipel6&rid=giphy.gif&ct=g')

    return ConversationHandler.END


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
    return PLAY


# Функция обработки не распознанных команд
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Неверная команда!\n"
                                  "\nСписок команд:\n"
                                  "/start | /play | /exit | /help")


help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

conv_handler = ConversationHandler(
    # Точка входа в разговор
    entry_points=[CommandHandler('start', start)],
    # Этапы разговора, каждый со своим списком обработчиков сообщений
    states={
        PLAY: [CommandHandler('play', play), CommandHandler('exit', exit_func), CommandHandler('help', help),
               CommandHandler('start', start)],
        GAME_CYCLE: [MessageHandler(Filters.text, game_cycle1)],
        RESULT: [MessageHandler(Filters.text, result)],
    },
    # Точка выхода из разговора
    fallbacks=[CommandHandler('exit', exit_func), CommandHandler('play', play)],
)

# Добавляем обработчик разговоров `conv_handler`
dispatcher.add_handler(conv_handler)

# Обработчик не распознанных команд. Должен быть обязательно в конце чтобы не перехватывать команды, которые идут раньше
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
updater.idle()
