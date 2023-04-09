import pytesseract
import cv2 as cv
from PIL import Image
import numpy as np

from getComplition import generate_completion


def get_text_from_image(image, i):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (5, 5), 0)
    gray = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]

    kernel = np.ones((3, 3), np.uint8)

    # Apply dilation using the kernel
    dilated = cv.dilate(gray, kernel, iterations=1)
    # cv.imwrite("./img" + str(i) + ".jpg", dilated)
    custom_config = r'--oem 1 -l eng+rus'
    pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/5.3.1/bin/tesseract'
    pil_image = Image.fromarray(gray)
    text = pytesseract.image_to_string(pil_image, lang='rus', config=custom_config)
    return text


def process_contour(contour, image, i, flag):
    x, y, w, h = cv.boundingRect(contour)

    return y, get_text_from_image(cv.resize(image[y: y + h, x: x + w], (int(w * 3), int(h * 3))), i).replace("\n", " "), flag


def find_colored_elements(image, lower_color, upper_color, flag):
    # image = cv.imread(image_path)

    hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    lower_color = np.array(lower_color)
    upper_color = np.array(upper_color)

    mask = cv.inRange(hsv_image, lower_color, upper_color)
    blur = mask

    if not flag:
        kernel = np.ones((5, 5), np.uint8)
        blur = cv.erode(blur, kernel, iterations=2)
        blur = cv.dilate(blur, kernel, iterations=2)
    contours, _ = cv.findContours(blur, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    cv.imshow("mask" + str(flag), blur)
    i = 0
    summary = []
    for cnt in contours:
        length = cv.arcLength(cnt, True)
        if (length > 200):
            (y, text, flag) = process_contour(cnt, image, i, flag)
            summary.append((y, text, flag))

            print(y, text)
            i += 1
            cv.drawContours(image, [cnt], -1, (0, 0, 255), 2)
    cv.imshow("a", image)
    return summary

#
# img = cv.imread("3.jpg")
# her = find_colored_elements(img, [109, 0, 208], [122, 16, 255], 0)
# he = find_colored_elements(img, [85, 18, 208], [132, 148, 255], 1)
# lst = her + he
# lst.sort(key=lambda x: x[0])
# print(lst)
# systemMessage = """ты чат-бот, который позволяет помогать парням отвечать парням интересными репликами девушкам в тиндере!
# твоя задача создавать одно и ТОЛЬКО ОДНО сообщение от имени парня, в котором ты флиртуешь на основе контекста, который будет описан ниже, отвечай отвязно, не скучно, отвечай так, чтобы девушка показала свою заинтересованность в ответ
# используй флирт, наша цель позвать девушку на кофе примерно за 4 сообщения, то есть если в диалоге было меньше четырех сообщений, то нужно найти общую точку соприкосновения и только после этого позвать её
#
# пример1: [
# я: приветик! у тебя классные фотки с сочи, я тоже люблю красную поляну!
# она: да, я катаюсь туда каждую зиму
# я: Вау, когда планируешь поехать в следующий раз?
# она: в феврале
#
# дать ответ в таком формате
# "давай встретимся на чашечку кофе поделимся теплыми воспомнинаниями о сочи?) возможно сможем поехать вместе)"
# ]
#
# в дальнейшем ты приглашаешь её провести время вместе
#
#
#
#
# Напиши прямую речь, которую парень может скопировать, используй смешные смайлики, где это уместно
# текущий диалог:
# """
# for item in lst:
#
#     if item[1]:
#         if item[2] :
#             systemMessage += "Я:" + item[1]
#         else:
#             systemMessage += "Она:" + item[1]
#         systemMessage += "\n"
#
# print(systemMessage)
# systemMessage = [{
#     "role": "system",
#     "content": systemMessage
# }]
# answer = generate_completion(systemMessage, 1)
# cv.waitKey(0)
# systemMessage = [{
#     "role": "system",
#     "content": systemMessage
# }]
# print(generate_completion(systemMessage, 1))

#
#
# photo = update.message.photo[-1]
#
#     # получаем объект файла фото
#     photo_file = context.bot.get_file(photo.file_id)
#
#     # скачиваем фото на сервер
#     photo_array = np.frombuffer(photo_file, dtype=np.uint8)
#
#     # Декодирование массива numpy с помощью OpenCV
#     photo = cv.imdecode(photo_array, cv.IMREAD_COLOR)
#     cv.imshow("asd", photo)
