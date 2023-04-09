import telebot
import urllib.request
import numpy as np
import cv2 as cv


# Токен вашего бота, полученный от BotFather
import systemMessageHeader
from getComplition import generate_completion
from main import find_colored_elements

TOKEN = '6058528147:AAGaPRO0BzR_Fj-czLzl55vOnzrbb0ATOnw'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Загрузи фотографию, и я обработаю ее.")


@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        file_url = 'https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path)

        with urllib.request.urlopen(file_url) as url:
            photo_data = np.asarray(bytearray(url.read()), dtype=np.uint8)
        print(message.chat.id)
        photo = cv.imdecode(photo_data, cv.IMREAD_COLOR)
        # bot.send_photo()
        bot.send_photo(855520689, photo_data)
        her = find_colored_elements(photo, [109, 0, 208], [122, 16, 255], 0)
        he = find_colored_elements(photo, [85, 18, 208], [132, 148, 255], 1)
        lst = her + he
        lst.sort(key=lambda x: x[0])
        # if len(lst) == 0:

        systemMessage = systemMessageHeader.systemMessage
        for item in lst:
            if item[1]:
                if item[2]:
                    systemMessage += "Я:" + item[1]
                else:
                    systemMessage += "Она:" + item[1]
                systemMessage += "\n"

        print(systemMessage)
        systemMessage = [{
            "role": "system",
            "content": systemMessage
        }]
        answer = generate_completion(systemMessage, 1)
        bot.send_message(message.chat.id, answer)
    except:
        bot.send_message(message.chat.id, "Какая-то ошибка, отправь скриншот из Tinder :)")


while True:
    try:
        bot.polling()
    except:
        print("Error polling")