import sys
import logging
from asyncio import run
from rembg import remove
from os import getenv, mkdir
from dotenv import load_dotenv
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from logging import basicConfig, INFO
from aiogram import Bot, Dispatcher, F
from PIL import Image, UnidentifiedImageError

basicConfig(level=INFO)
load_dotenv('.env')
BOT_TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()


def create_path():
    try:
        mkdir('input_images')
        mkdir('output_images')
    except FileExistsError:
        pass


@dp.message(F.document)
async def files_handler(message: Message) -> None:
    """Remove background function"""
    create_path()
    try:
        input_img = await message.bot.get_file(message.document.file_id)
        await message.bot.download_file(input_img.file_path, f'input_images/{message.document.file_id}.png')

        img_editing = remove(Image.open(f'input_images/{message.document.file_id}.png'))
        img_editing.save(f'output_images/{img_editing}.png')

        output_img = FSInputFile(f'output_images/{img_editing}.png')
        await message.answer_document(output_img, caption="Вуаля!")
    except UnidentifiedImageError:
        await message.answer("Для редактирования необходимо отправить изображение в виде файла!")
    except FileNotFoundError:
        await message.answer("Что-то пошло не так... Обратитесь к админу!")


@dp.message()
async def echo_handler(message: Message) -> None:
    """Other message handling function"""
    await message.answer("Для редактирования необходимо отправить изображение в виде файла!")


async def main() -> None:
    """Entry point"""
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    run(main())
