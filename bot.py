import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is not set")

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()

UPPERCASE = "🔤 UPPERCASE"
LOWERCASE = "🔡 lowercase"
TITLE_CASE = "✨ Title Case"

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=UPPERCASE)],
        [KeyboardButton(text=LOWERCASE)],
        [KeyboardButton(text=TITLE_CASE)],
    ],
    resize_keyboard=True,
    is_persistent=True,
)


def convert_title_case(text: str) -> str:
    return " ".join(word.capitalize() for word in text.split())


@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(
        "👋 <b>Welcome to XRootsec!</b>\n\n"
        "Change the case of your text quickly and easily. Send a word, sentence, or paragraph, "
        "then choose one of the three tools below.\n\n"
        "<b>Sample:</b>\n"
        "hello world from xrootsec\n\n"
        "Try <b>UPPERCASE</b>, <b>lowercase</b>, or <b>Title Case</b> to format your text.",
        reply_markup=keyboard,
    )


@dp.message(F.text == UPPERCASE)
async def uppercase_handler(message: Message) -> None:
    await message.answer(
        "Send the text you want to convert, then press <b>UPPERCASE</b>.",
        reply_markup=keyboard,
    )


@dp.message(F.text == LOWERCASE)
async def lowercase_handler(message: Message) -> None:
    await message.answer(
        "Send the text you want to convert, then press <b>lowercase</b>.",
        reply_markup=keyboard,
    )


@dp.message(F.text == TITLE_CASE)
async def title_case_handler(message: Message) -> None:
    await message.answer(
        "Send the text you want to convert, then press <b>Title Case</b>.",
        reply_markup=keyboard,
    )


@dp.message(F.text)
async def text_handler(message: Message) -> None:
    text = (message.text or "").strip()
    if not text:
        await message.answer("Please send some text to get started.", reply_markup=keyboard)
        return

    await message.answer(
        "✅ <b>Text received!</b>\n\n"
        f"<b>Sample:</b>\n{text}\n\n"
        "Choose a button below to change the text case.",
        reply_markup=keyboard,
    )


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
