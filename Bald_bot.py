import asyncio
import logging
import sys
import numpy as np


from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
import tensorflow as tf
from tensorflow.keras.preprocessing import image

loaded_model = tf.keras.models.load_model('BaldModel.h5')

def preprocess_images(path):
    img = image.load_img(path, target_size=(178, 218))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_preprocessed = img_array / 255.0
    
    return img_preprocessed

def test (img_path):
    img = preprocess_images(img_path)
    prediction = loaded_model.predict(img)
    predicted_class_index = np.argmax(prediction)

    class_labels = ['bald', 'notbald'] 
    predicted_class_label = class_labels[predicted_class_index]
    if predicted_class_label == 'bald':
        return 1
    else:
        return 0


dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")

@dp.message(F.photo)
async def photo_handler(message: Message) -> None:
    await message.bot.download(file=message.photo[-1].file_id, destination='test.jpg')

    if test("test.jpg") == 1:
        await message.answer(f"Bald")
    else:
        await message.answer(f"Not Bald")


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.answer("Nice try!")
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    bot = Bot(token="7374998044:AAE2PF7floF0cFbJYX95zswxgPFqZ3uEtWc", default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
