from flask import Flask
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
import logging
import asyncio
from datetime import datetime
import os

# Инициализация Flask (keep_alive)
app = Flask(__name__)

@app.route('/')
def index():
    return "I'm alive!"

# Константы
API_TOKEN = '7672403214:AAGeYafr1OsdF2puiEzOyfMyFP8HTKmBta8'
ADMIN_CHAT_ID = -1002859466060

# Настройка логирования и бота
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

# --- Стратегии дня ---
strategies = [
    "🎯 Ставь на live-тоталы после 10-й минуты — анализируй динамику матча!",
    "📊 Используй догон на ничью в лайве — особенно в равных по силам лигах.",
    "🚀 Перестраховка: ставь 70% на фаворита и 30% на ничью в двойных шансах.",
    "📉 Играем на понижение: тотал меньше в затяжных матчах с малым количеством ударов.",
    "🔥 Стратегия 5+5: пять ставок в день по 2% от банка с разными типами исходов.",
]

# --- Клавиатуры ---
main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📈 Стратегия дня"), KeyboardButton(text="🎁 Получить купон")],
    [KeyboardButton(text="📝 Регистрация"), KeyboardButton(text="📣 Наш Telegram")],
    [KeyboardButton(text="🌍 Вход на сайт"), KeyboardButton(text="🛟 Поддержка")]
], resize_keyboard=True)

back_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🔙 Назад")]], resize_keyboard=True)
back_ready_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="✅ Готово")],
    [KeyboardButton(text="🔙 Назад")]
], resize_keyboard=True)

# --- Обработчики сообщений ---
@router.message(F.text == "/start")
async def start_cmd(message: types.Message):
    await message.answer("👋 Привет! Добро пожаловать в Pro Stavki | Profit Bot.", reply_markup=main_menu)

@router.message(F.text == "📈 Стратегия дня")
async def strategy_day(message: types.Message):
    day_index = datetime.now().day % len(strategies)
    await message.answer(f"📊 Стратегия на сегодня:\n{strategies[day_index]}", reply_markup=back_menu)

@router.message(F.text == "🌍 Вход на сайт")
async def open_site(message: types.Message):
    await message.answer("🌐 Открывай [наш сайт](https://pro-stavki-site.onrender.com/)", parse_mode="Markdown", disable_web_page_preview=True, reply_markup=back_menu)

@router.message(F.text == "📝 Регистрация")
async def registration_link(message: types.Message):
    await message.answer("🔑 [Регистрируйся здесь](https://1wvteh.com/?p=7bd0)", parse_mode="Markdown", disable_web_page_preview=True, reply_markup=back_ready_menu)

@router.message(F.text == "📣 Наш Telegram")
async def telegram_channel(message: types.Message):
    await message.answer("📢 Присоединяйся к нашему [каналу](https://t.me/ProStavki_365)", parse_mode="Markdown", disable_web_page_preview=True, reply_markup=back_menu)

@router.message(F.text == "🛟 Поддержка")
async def support_link(message: types.Message):
    await message.answer("💬 Пиши [в поддержку](https://t.me/ProStavki365)", parse_mode="Markdown", disable_web_page_preview=True, reply_markup=back_menu)

@router.message(F.text == "🎁 Получить купон")
async def get_coupon(message: types.Message):
    await message.answer("🎯 Для получения купона:\n1. Зарегистрируйся\n2. Пополни счёт\n3. Отправь скрин или ID депозита сюда.", reply_markup=back_ready_menu)

@router.message(F.text == "✅ Готово")
async def done_handler(message: types.Message):
    await message.answer("📩 Ждём подтверждение (скриншот или ID).", reply_markup=back_menu)

@router.message(F.text == "🔙 Назад")
async def go_back(message: types.Message):
    await message.answer("🔙 Возвращаюсь в главное меню:", reply_markup=main_menu)

@router.message(F.photo)
async def handle_photo(message: types.Message):
    await message.answer("📥 Лови [гайд в PDF](https://drive.google.com/file/d/1W5n5cQ19ktQwxa87GWHog3yWL2z9mBXy/view?usp=sharing)", parse_mode='Markdown', reply_markup=main_menu)
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"📸 Скриншот от @{message.from_user.username} (ID: {message.from_user.id})")

@router.message(F.text.regexp(r"^ID\d{4,}").as_('deposit'))
async def handle_deposit_id(message: types.Message, deposit: types.Message):
    user_input = deposit.text.strip().upper()
    await message.answer(f"✅ Депозит под {user_input} подтверждён!\n📥 Лови [PDF-гайд](https://drive.google.com/file/d/1W5n5cQ19ktQwxa87GWHog3yWL2z9mBXy/view?usp=sharing)", parse_mode='Markdown', reply_markup=main_menu)
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"✅ Подтверждение от @{message.from_user.username} — {user_input}")

# --- Запуск бота и сервера ---
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    import threading

    def run_flask():
        app.run(host="0.0.0.0", port=8080)

    threading.Thread(target=run_flask).start()

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")
