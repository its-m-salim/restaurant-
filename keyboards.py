from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from service import *





main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🍽 Меню"), KeyboardButton(text="❓ Помощь")],
        [KeyboardButton(text="🔐 Войти как администратор")]
    ],
    resize_keyboard=True,
)




admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🍽 Меню"), KeyboardButton(text="➕ Добавить блюдо")],
        [KeyboardButton(text="🗑 Удалить блюдо"), KeyboardButton(text="📋 Список блюд")],
        [KeyboardButton(text="❓ Помощь"), KeyboardButton(text="📦 Заказы")],
        [KeyboardButton(text="➕ Добавить категорию"), KeyboardButton(text="✏️ Изменить")]
    ],
    resize_keyboard=True,
)

cancel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
])



async def get_category_btn():
    data = await get_categories()
    keyboards = []

    for ct in data:
        keyboards.append([InlineKeyboardButton(text=ct['name'], callback_data=f"category_{ct['id']}")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)
    return keyboard



async def get_ct_dishes_btn(cat_id):
    data = await get_category_dishes(cat_id)
    keyboards = []

    for dish in data:
        keyboards.append([InlineKeyboardButton(text=dish['name'], callback_data=f"dish_{dish['id']}")])

    keyboards.append([InlineKeyboardButton(text="⬅️ К категориям", callback_data="back_categories")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)
    return keyboard




async def get_order_btn():
    keyboards =  [
        [InlineKeyboardButton(text="🛒 Заказать", callback_data="new_order")],
        [InlineKeyboardButton(text="⬅️ К категориям", callback_data="back_categories")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)
    return keyboard



async def get_dishes_all_btn():
    data = await get_all_dishes()
    keyboards = []

    for index, dish in enumerate(data, start=1):
        keyboards.append([InlineKeyboardButton(text=f"{index}. {dish['name']}", callback_data=f"dishd_{dish['id']}")])

    keyboards.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)
    return keyboard



async def get_new_dish_ct():
    data = await get_categories()
    keyboards = []

    for ct in data:
        keyboards.append([InlineKeyboardButton(text=ct['name'], callback_data=f"dishct_{ct['id']}")])

    keyboards.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)
    return keyboard



async def get_delete_confirm_btn(dish_id):
    keyboards = [
        [InlineKeyboardButton(text="✅ Да, удалить", callback_data=f"confirm_delete_{dish_id}"),
        InlineKeyboardButton(text="❌ Нет", callback_data="cancel")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)
    return keyboard




async def get_edit_options():

    keyboards = [
        [InlineKeyboardButton(text="Категория", callback_data="edit_ct"), InlineKeyboardButton(text="Имя", callback_data="edit_name")],
        [InlineKeyboardButton(text="Описание", callback_data="edit_caption"), InlineKeyboardButton(text="Цена", callback_data="edit_price")],
        [InlineKeyboardButton(text="Фото", callback_data="edit_photo")]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)

    return keyboard



async def get_dishes_edit_btn():
    data = await get_all_dishes()
    keyboards = []

    for index, dish in enumerate(data, start=1):
        keyboards.append([InlineKeyboardButton(text=f"{index}. {dish['name']}", callback_data=f"dishe_{dish['id']}")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)
    return keyboard



async def get_edit_categoires():
    data = await get_categories()
    keyboards = []

    for ct in data:
        keyboards.append([InlineKeyboardButton(text=ct['name'], callback_data=f"categorye_{ct['id']}")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)
    return keyboard
