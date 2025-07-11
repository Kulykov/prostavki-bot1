from keep_alive import keep_alive
keep_alive()

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
import logging, asyncio
from datetime import datetime

API_TOKEN = '7672403214:AAGeYafr1OsdF2puiEzOyfMyFP8HTKmBta8'
ADMIN_CHAT_ID = -1002859466060

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

strategies = [ ... ]  # Твой список стратегий

main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📈 Стратегия дня"), KeyboardButton(text="🎁 Получить купон")],
    [KeyboardButton(text="🛟 Поддержка"), KeyboardButton(text="📝 Регистрация")],
    [KeyboardButton(text="📣 Наш Telegram")]
], resize_keyboard=True)

back_menu = ReplyKeyboardMarkup([[KeyboardButton("🔙 Назад")]], resize_keyboard=True)
back_ready = ReplyKeyboardMarkup([
    [KeyboardButton("✅ Готово"), KeyboardButton("🔙 Назад")]
], resize_keyboard=True)

@router.message(F.text == "/start")
async def start_cmd(message: types.Message):
    await message.answer("👋 Приветствуем в ProStavki | Profit! ...", reply_markup=main_menu)

# — все остальные хендлеры, как прежде…

if __name__ == '__main__':
    async def main():
        dp.include_router(router)
        await dp.start_polling(bot)
    asyncio.run(main())
