from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = '8221559500:AAEcJyUH8_h7CtQhlcXzchuaqu28rBVwqLI'  # вставь сюда свой токен
OWNER_ID = 870514707           # вставь сюда свой Telegram ID

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Главное меню — выбор целей
purpose_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
purpose_keyboard.add(
    KeyboardButton("🔁 Автоответчик"),
    KeyboardButton("🛍️ Интернет-магазин"),
    KeyboardButton("📩 Рассылка"),
)
purpose_keyboard.add(
    KeyboardButton("📝 Приём заявок"),
    KeyboardButton("⚙️ Свой вариант")
)

# Клавиатура да/нет
payment_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
payment_keyboard.add(
    KeyboardButton("✅ Да, нужна оплата"),
    KeyboardButton("❌ Нет, без оплаты")
)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer(
        "👋 Привет! Я помогу тебе заказать бота.\n\nВыбери, для каких целей тебе нужен бот:",
        reply_markup=purpose_keyboard
    )
    await bot.send_message(
        OWNER_ID,
        f"🔔 Новый пользователь @{message.from_user.username or 'без username'} запустил бота."
    )


@dp.message_handler(lambda msg: msg.text in [
    "🔁 Автоответчик", "🛍️ Интернет-магазин", "📩 Рассылка", "📝 Приём заявок", "⚙️ Свой вариант"
])
async def handle_purpose(message: types.Message):
    purpose = message.text
    await message.answer("💳 Нужна ли оплата внутри бота?", reply_markup=payment_keyboard)
    # сохраняем выбор пользователя (можно заменить на БД, если нужно)
    user_data[message.from_user.id] = {'purpose': purpose}

user_data = {}


@dp.message_handler(lambda msg: msg.text in ["✅ Да, нужна оплата", "❌ Нет, без оплаты"])
async def handle_payment_choice(message: types.Message):
    payment = message.text
    user_id = message.from_user.id
    data = user_data.get(user_id, {})
    purpose = data.get('purpose', 'Не указано')

    await message.answer("✅ Спасибо! Мы свяжемся с вами для обсуждения деталей.")

    await bot.send_message(
        OWNER_ID,
        f"📬 Заявка от @{message.from_user.username or 'без username'}\n"
        f"🆔 ID: {user_id}\n"
        f"🎯 Цель бота: {purpose}\n"
        f"💰 Оплата в боте: {'Да' if 'Да' in payment else 'Нет'}"
    )


@dp.message_handler()
async def fallback(message: types.Message):
    await message.answer("Выберите вариант из предложенных кнопок 👇")


if __name__ == '__main__':
    print("🤖 БОТ ЗАПУЩЕН")
    executor.start_polling(dp, skip_updates=True)