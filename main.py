import telebot
import redis

bot = telebot.TeleBot('8151764446:AAH2toiVYr0PwmkRKWDNFYRMF1PHefcQR2o')
r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)


# Метод для получения текстовых сообщений
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/reg":
        bot.send_message(message.from_user.id, "Привет, как тебя зовут?")
        bot.register_next_step_handler(message, get_name)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши /reg!")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


def get_name(message):
    global name 
    name = message.text
    bot.send_message(message.from_user.id, "Какое у тебя хобби?")
    bot.register_next_step_handler(message, get_hobby)

def get_hobby(message):
    global hobby
    hobby = message.text
    bot.send_message(message.from_user.id, f"Привет, {name}! Тебе нравится {hobby}!")

    r.set(name, hobby)
    bot.send_message(message.from_user.id, f"Ты успешно добавлен в redis!!!")
    bot.send_message(message.from_user.id, "Хочешь посмотреть что нравится остальным пользователям?")
    bot.register_next_step_handler(message, show_users)


def show_users(message):
    if message.text == 'Да':
        data = ''
        for key in r.scan_iter():
            data += f'{key} любит {r.get(key)}\n'
        bot.send_message(message.from_user.id, f"{data}")
    bot.send_message(message.from_user.id, f"Хорошего дня! :)")



bot.polling(none_stop=True, interval=0)