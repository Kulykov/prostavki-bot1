import logging
import os
from datetime import datetime
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Установи свой токен в переменную окружения
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

# --- Стратегии ставок на спорт ---
sport_strategies = [
    "1️⃣ **Ставка на фору команды А**\nЕсли команда А играет дома против аутсайдера, можно поставить на фору -1. Это даёт выигрыш даже при минимальной победе. Используйте, если команда имеет хорошую форму и статистику побед на домашнем поле.",
    "2️⃣ **Тотал больше 2.5 голов**\nСтавка на то, что обе команды забьют в сумме более 2 голов. Работает на матчах атакующего типа. Проверяйте последние 5-10 игр команд.",
    "3️⃣ **Двойной шанс на фаворита**\nВы выбираете, что фаворит либо победит, либо сыграет вничью. Снижает риск проигрыша в матчах с непредсказуемым аутсайдером.",
    "4️⃣ **Обе команды забьют**\nСтавка на то, что обе команды забьют хотя бы один гол. Работает на матчах с сильными атакующими командами.",
    "5️⃣ **Фора + Тотал меньше 3.5**\nСтавка на сильного фаворита с отрицательной форой и ограниченным количеством голов. Минимизирует риск крупного проигрыша.",
    "6️⃣ **Ставка на ничью**\nРаботает на матчах равных по силе команд. Особенно эффективна при ставках на ничью с форой или в лайве.",
    "7️⃣ **Овертайм/дополнительное время**\nИспользуется для ставок на исход после основного времени. Часто применяется в хоккее и баскетболе.",
    "8️⃣ **Корнеры и карточки**\nСтавки на количество угловых и карточек. Полезно для аналитиков статистики команд.",
    "9️⃣ **Ставка на лучший тайм**\nВыбор победителя первого или второго тайма. Можно комбинировать с тоталом.",
    "🔟 **Экспресс на фаворитов**\nОбъединяем несколько фаворитов в одну ставку для увеличения коэффициента. Высокий риск, но и потенциальная прибыль больше.",
]

# --- Стратегии казино ---
casino_strategies = [
    "1️⃣ **Рулетка: стратегия Мартингейл**\nУдваиваем ставку после каждого проигрыша на равные шансы (чёт/нечёт). Цель — вернуть все потери и получить прибыль после выигрыша. Требуется достаточный банк для серий проигрышей.",
    "2️⃣ **Рулетка: стратегия Лабушер**\nЗаписываем ряд чисел, сумма которых — желаемая прибыль. Ставим сумму первой и последней цифры ряда. Если выиграли — зачёркиваем числа, если проиграли — добавляем сумму в конец ряда.",
    "3️⃣ **Рулетка: стратегия Пароли**\nУдваиваем ставку после выигрыша, а не после проигрыша. Цель — использовать удачные серии и фиксировать прибыль. Работает на коротких сериях.",
    "4️⃣ **Крэпс: стратегия 3-2-1**\nСтавки на пассы и линии с прогрессивным управлением. Ставка уменьшается после выигрыша и увеличивается после проигрыша.",
    "5️⃣ **Блэкджек: базовая стратегия**\nСледуем таблице оптимальных действий: брать карту, стоять, удваивать или разделять. Минимизирует преимущество казино.",
    "6️⃣ **Слот-машины: стратегия ставок**\nСтавим максимум на бонусные игры и бесплатные вращения. Используем короткие серии ставок для контроля бюджета.",
    "7️⃣ **Покер: стратегия тайтово-агрессивная**\nИграем с узким диапазоном сильных рук, агрессивно повышая ставки при сильной позиции.",
    "8️⃣ **Покер: стратегия блёфа**\nИспользуем тщательно продуманные блефы в нужные моменты, наблюдая за поведением оппонентов.",
    "9️⃣ **Баккара: стратегия 1-3-2-6**\nПрогрессивная система ставок для серии выигрышей. Помогает фиксировать прибыль и уменьшать потери.",
    "🔟 **Рулетка: случайные числа**\nВыбираем числа наугад или любимые числа. Это классическая стратегия без анализа, но с интересным азартом.",
]

# --- Главное меню ---
def main_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text="🎯 Стратегия дня", callback_data="strategy"),
        InlineKeyboardButton(text="🎁 Бонус", callback_data="bonus"),
        InlineKeyboardButton(text="🎮 Игры", callback_data="games"),
        InlineKeyboardButton(text="📢 Наш Telegram", url="https://t.me/ProStavki_365"),
        InlineKeyboardButton(text="🆘 Поддержка", url="https://t.me/ProStavki365"),
    ]
    keyboard.add(*buttons)
    return keyboard

# --- Клавиатура возврата ---
def back_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="back"))
    return keyboard

# --- Команда /start ---
@dp.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Добро пожаловать в наш бот.\n\n"
        "Выбери действие из меню ниже ⬇️",
        reply_markup=main_menu()
    )

# --- Стратегия дня ---
@dp.callback_query(lambda c: c.data == "strategy")
async def strategy_handler(callback: types.CallbackQuery):
    today = datetime.now().day
    sport_strategy = sport_strategies[today % len(sport_strategies)]
    casino_strategy = casino_strategies[today % len(casino_strategies)]

    await callback.message.answer(
        f"📌 Стратегия дня ({datetime.now().date()}):\n\n"
        f"🎯 Ставки на спорт:\n{sport_strategy}\n\n"
        f"🎰 Казино:\n{casino_strategy}",
        reply_markup=back_menu()
    )
    await callback.answer()

# --- Кнопка бонуса ---
@dp.callback_query(lambda c: c.data == "bonus")
async def bonus_handler(callback: types.CallbackQuery):
    bonus_text = (
        "💰 Получай бонус до **15 000 ₽** для ставок на спорт и казино!\n\n"
        "Используй его и увеличь свои шансы на выигрыш! 🎯🎰"
    )
    
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="💎 Забрать бонус", url="https://1wtsaw.life/casino/list/4?p=lwpw"),
        InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="back")
    )
    
    await callback.message.answer(bonus_text, reply_markup=keyboard)
    await callback.answer()

# --- Кнопка игры ---
@dp.callback_query(lambda c: c.data == "games")
async def games_handler(callback: types.CallbackQuery):
    text = (
        "🎮 Добро пожаловать в раздел игр!\n\n"
        "Здесь ты можешь выбрать любимую игру и испытать удачу! 🍀"
    )
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="✈️ Aviator", url="https://1wtsaw.life/casino/list/4?p=lwpw"),
        InlineKeyboardButton(text="💣 Mines", url="https://1wtsaw.life/casino/list/4?p=lwpw"),
        InlineKeyboardButton(text="📈 Plinko", url="https://1wtsaw.life/casino/list/4?p=lwpw"),
        InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="back")
    )
    await callback.message.answer(text, reply_markup=keyboard)
    await callback.answer()

# --- Кнопка возврата ---
@dp.callback_query(lambda c: c.data == "back")
async def back_handler(callback: types.CallbackQuery):
    await callback.message.answer("Главное меню ⬇️", reply_markup=main_menu())
    await callback.answer()

# --- Запуск бота ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
