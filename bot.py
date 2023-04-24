import urllib.request
import numpy as np
import cv2 as cv
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware

import systemMessageHeader
from getComplition import generate_completion
from main import find_colored_elements

TOKEN = '6058528147:AAGaPRO0BzR_Fj-czLzl55vOnzrbb0ATOnw'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


async def worker(queue: asyncio.Queue):
    while True:
        task = await queue.get()

        if task is None:
            break

        message, photo_data = task
        try:
            answer = await process_photo(photo_data)
            await bot.send_message(message.chat.id, answer)
        except Exception as e:
            print(e)
            await bot.send_message(message.chat.id, "Какая-то ошибка, отправь скриншот из Tinder :)")

        queue.task_done()


async def create_workers(n, queue):
    tasks = []
    for _ in range(n):
        task = asyncio.create_task(worker(queue))
        tasks.append(task)
    return tasks


async def download_image(file_id):
    file_info = await bot.get_file(file_id)
    file_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}'

    with urllib.request.urlopen(file_url) as url:
        photo_data = np.asarray(bytearray(url.read()), dtype=np.uint8)

    return photo_data


# @dp.message_handler(content_types=['photo'])
# async def photo_handler(message: types.Message):
#     photo_data = await download_image(message.photo[-1].file_id)
#     await task_queue.put((message, photo_data))



@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.chat.id, "Привет! Загрузи фотографию, и я обработаю ее.")




from concurrent.futures import ThreadPoolExecutor


def process_photo(photo_data):
    photo = cv.imdecode(photo_data, cv.IMREAD_COLOR)
    her = find_colored_elements(photo, [109, 0, 208], [122, 16, 255], 0)
    he = find_colored_elements(photo, [85, 18, 208], [132, 148, 255], 1)
    lst = her + he
    lst.sort(key=lambda x: x[0])

    systemMessage = systemMessageHeader.systemMessage
    for item in lst:
        if item[1]:
            if item[2]:
                systemMessage += "Я:" + item[1]
            else:
                systemMessage += "Она:" + item[1]
            systemMessage += "\n"

    systemMessage = [{
        "role": "system",
        "content": systemMessage
    }]
    return generate_completion(systemMessage, 1)


ex = ThreadPoolExecutor()


async def process_and_send_result(message, photo_data):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(ex, process_photo, photo_data)
    await bot.send_message(chat_id=message.chat.id, text=result)


@dp.message_handler(content_types=['photo'])
async def photo_handler(message: types.Message):
    photo_data = await download_image(message.photo[-1].file_id)
    print(message.photo[-1].file_id)
    # Создаем асинхронную задачу для обработки фотографии и отправки результата
    processing_task = asyncio.create_task(process_and_send_result(message, photo_data))

    # Не ждем завершения задачи, чтобы бот мог продолжать обрабатывать другие сообщения
    await task_queue.put((message, photo_data))
# @dp.message_handler(content_types=['photo'])
# async def photo_handler(message: types.Message):
#     try:
#         start = datetime.datetime.now()
#         photo_data = await download_image(message.photo[-1].file_id)
#         answer = await process_photo(photo_data)
#         await bot.send_message(message.chat.id, answer)
#
#     except Exception as e:
#         print(e)
#         await bot.send_message(message.chat.id, "Какая-то ошибка, отправь скриншот из Tinder :)")

task_queue = asyncio.Queue()
worker_tasks = None


async def on_shutdown(dp):
    for _ in range(len(worker_tasks)):
        task_queue.put_nowait(None)

    await task_queue.join()

    for task in worker_tasks:
        task.cancel()

    await dp.storage.close()
    await dp.storage.wait_closed()

    await bot.close()

async def main():
    worker_tasks = await create_workers(4, task_queue)
    try:
        await dp.start_polling()
    finally:
        await on_shutdown(dp)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    finally:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(on_shutdown(dp))
