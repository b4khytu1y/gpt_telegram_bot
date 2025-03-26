import os
import openai
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()
logging.basicConfig(level=logging.INFO)

# Правильно получаем токены
TELEGRAM_BOT_TOKEN = os.getenv("8025483084:AAH_CgKKebA0UUi_mKEKzk82YenNSQ2Li4M")
OPENAI_API_KEY = os.getenv("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")


# Устанавливаем ключ OpenAI
openai.api_key = OPENAI_API_KEY

# Создаем экземпляры бота и диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Функция общения с GPT
async def get_gpt_reply(user_message: str) -> str:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты весёлый и дружелюбный помощник по имени Паймон."},
                {"role": "user", "content": user_message},
            ]
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Ошибка GPT: {e}"

# Обработка команды /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я Паймон, твой напарник! 🎉 Напиши мне что-нибудь!")

# Обработка обычных сообщений
@dp.message()
async def chat(message: Message):
    await message.answer("⌛ Думаю...")
    reply = await get_gpt_reply(message.text)
    await message.answer(reply)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
