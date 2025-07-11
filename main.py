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

# --- Стратегии по дням ---
strategies = [
    "🎯 Ставь на live-тоталы после 10-й минуты — анализируй динамику матча!",
    "📊 Используй догон на ничью в лайве — особенно в равных по силам лигах.",
    "🚀 Перестраховка: ставь 70% на фаворита и 30% на ничью в двойных шансах.",
    "📉 Играем на понижение: тотал меньше в затяжных матчах с малым количеством ударов.",
    "🔥 Стратегия 5+5: пять ставок в день по 2% от банка с разными типами исходов.",
    "💼 Используй вилки между букмекерами для минимального, но стабильного дохода.",
    "🎯 Делай ставки в лайве после удаления — коэффициенты растут, а шанс предсказуем!",
    "📈 Ставь только на проверенные команды — избегай низших лиг без статистики.",
    "🧠 Анализируй предыдущие встречи команд — это часто ключ к победе.",
    "⏱ Лучшее время — последние 15 минут тайма: коэффициенты максимальные.",
    "📉 Используй обратную психологию: если все ставят на одно — подумай иначе.",
    "🔁 Делай перерыв раз в неделю — свежая голова = свежие победы.",
    "📦 Экспрессы? Да, но максимум из 2 событий с высоким ROI.",
    "⚽ Не ставь по эмоциям — только холодный расчёт и статистика.",
    "🧾 Следи за банком — фиксированная ставка = контроль и стабильность."
]

# --- Клавиатуры ---
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📈 Стратегия дня"), KeyboardButton(text="🎁 Получить купон")],
        [KeyboardButton(text="🛟 Поддержка"), KeyboardButton(text="📝 Регистрация")],
        [KeyboardButton(text="📣 Наш Telegram")]
    ],
    resize_keyboard=True
)

back_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🔙 Назад")]],
    resize_keyboard=True
)

back_ready_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Готово"), KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True
)

# --- Обработчики ---
@router.message(F.text == "/start")
async def start_cmd(message: types.Message):
    await message.answer(
        "👋 Приветствуем в ProStavki | Profit! Здесь ты найдёшь лучшие стратегии, бонусы и эксклюзивный гайд.",
        reply_markup=main_menu)

@router.message(F.text == "📈 Стратегия дня")
async def strategy_day(message: types.Message):
    day_index = datetime.now().day % len(strategies)
    await message.answer(f"📊 Стратегия на сегодня:\n{strategies[day_index]}",
                         reply_markup=back_menu)

@router.message(F.text == "📝 Регистрация")
async def create_account(message: types.Message):
    await message.answer(
        "🔑 [Зарегистрируйся](https://1wjpvy.life/?p=7bd0) и получи бонус до 30 000₽ — начни путь к профиту!",
        reply_markup=back_ready_menu,
        disable_web_page_preview=True,
        parse_mode='Markdown')

@router.message(F.text == "🛟 Поддержка")
async def support(message: types.Message):
    await message.answer(
        "💬 [Связаться с админом](https://t.me/ProStavki365) — ответим на любой вопрос!",
        reply_markup=back_menu,
        disable_web_page_preview=True,
        parse_mode='Markdown')

@router.message(F.text == "📣 Наш Telegram")
async def channel_link(message: types.Message):
    await message.answer(
        "📢 Следи за новостями и прогнозами в [нашем канале](https://t.me/ProStavki_365)!",
        reply_markup=back_menu,
        disable_web_page_preview=True,
        parse_mode='Markdown')

@router.message(F.text == "🎁 Получить купон")
async def get_coupon(message: types.Message):
    await message.answer(
        "🎯 Для получения купона: 1) зарегистрируйся, 2) пополни счёт, 3) отправь скрин или ID депозита сюда.",
        reply_markup=back_ready_menu)

@router.message(F.text == "✅ Готово")
async def done_handler(message: types.Message):
    await message.answer(
        "📩 Отлично! Ждём подтверждение в виде скриншота или ID депозита.",
        reply_markup=back_menu)

@router.message(F.text == "🔙 Назад")
async def go_back(message: types.Message):
    await message.answer("🔙 Возвращаюсь в главное меню:",
                         reply_markup=main_menu)

@router.message(F.photo)
async def handle_photo(message: types.Message):
    await message.answer(
        "🔍 Смотрим скрин...\n📥 Вот твой [гайд в PDF](https://drive.google.com/file/d/1W5n5cQ19ktQwxa87GWHog3yWL2z9mBXy/view?usp=sharing)",
        parse_mode='Markdown',
        disable_web_page_preview=True,
        reply_markup=main_menu)
    await bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"📥 Новый скрин от @{message.from_user.username} (ID: {message.from_user.id})"
    )

@router.message(F.text.regexp(r"^ID\\d{4,}").as_('deposit'))
async def handle_deposit_id(message: types.Message, deposit: types.Message):
    user_input = deposit.text.strip().upper()
    if user_input.startswith("ID"):
        await message.answer(
            f"✅ Депозит под ID {user_input} подтверждён!\n📥 Лови [PDF-гайд](https://drive.google.com/file/d/1W5n5cQ19ktQwxa87GWHog3yWL2z9mBXy/view?usp=sharing)",
            parse_mode='Markdown',
            disable_web_page_preview=True,
            reply_markup=main_menu)
        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"✅ @{message.from_user.username} подтвердил депозит: {user_input}"
        )

# --- Запуск ---
if __name__ == '__main__':
    async def main():
        dp.include_router(router)
        await dp.start_polling(bot)

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")
