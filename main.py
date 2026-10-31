import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboards import *
from states import router as state_router
from service import *
from connection import *

load_dotenv()


token_bot = os.getenv("BOT_TOKEN")



bot = Bot(token=token_bot)


dp = Dispatcher()

@dp.message(Command("start"))
async def start_bot(message: Message):
    usr = message.from_user
    user = await profile(usr.id)

    if not user:
        if not await create_user(usr.username, usr.full_name, usr.id):
            await message.answer("⚠️ Не удалось зарегистрировать вас. Попробуйте позже.")
            return
        user = await profile(usr.id)
        password = usr.username or "admin13q"
        await set_password(password, usr.id)


    if user and user['is_admin']:
        await message.answer(
            "🛠 Добро пожаловать в панель администратора!\n\n"
            "Здесь вы можете управлять меню ресторана.",
            reply_markup=admin_kb,
        )
    else:

        await message.answer(
            f"👋 Добро пожаловать в наш ресторан, {usr.full_name}!\n\n"
            "🍽 Выбирайте блюда из меню и оформляйте заказ прямо здесь.",
            reply_markup=main_kb,
        )



@dp.message(F.text == "Заказы")
async def get_all_orders(message: Message):

    orders = await  g_orders()
    if not orders:
        await message.answer("Пока нет заказов")
        return

    text = "📋 <b>Список всех заказов</b>\n\n"

    for o in orders:
        text += f"""
🍽 <b>Блюдо:</b> {o['dish']}
🔢 <b>Количество:</b> {o['quantity']}
🪑 <b>Столик:</b> №{o['table_number']}
👤 <b>Заказчик:</b> {o['customer_name']}
🕒 <b>Время заказа:</b> {o['created_at']}

━━━━━━━━━━━━━━━━━━
"""

    await message.answer(text, parse_mode="HTML")



@dp.message(F.text == "🍽 Меню")
@dp.message(Command("menu"))
async def show_menu(message: Message):

    categories = await get_category_btn()

    if len(categories.inline_keyboard) <= 1:
        await message.answer("📭 Категории пока не добавлены.")
        return
    
    await message.answer("🍽 Выберите категорию:", reply_markup=categories)



@dp.message(F.text == "❓ Помощь")
@dp.message(Command("help"))
async def help_message(message: Message):

    await message.answer(
        "ℹ️ Помощь\n\n"
        "🍽 Меню — просмотр категорий и блюд.\n"
        "🛒 Заказать — оформление заказа: количество, номер столика и имя.\n"
        "❌ Отмена — прервать текущее действие.\n\n"
        "Для начала работы используйте /start.",
    )












async def main():
    print("Бот запущен")
    await create_tables()
    dp.include_router(state_router)
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())
