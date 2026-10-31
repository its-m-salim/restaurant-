from decimal import Decimal, InvalidOperation
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from service import *
from keyboards import *

router = Router()

class get_order(StatesGroup):
    get_order_count = State()
    get_order_table = State()
    get_order_name = State()

class delete_dish(StatesGroup):
    get_dish_id = State()


class Login(StatesGroup):
    password = State()



class add_category(StatesGroup):
    get_name = State()




class add_new_dish(StatesGroup):
    get_dish_category = State()
    get_dish_name = State()
    get_dish_caption = State()
    get_dish_price = State()
    get_dish_photo = State()



async def is_admin_user(user_id):
    user = await profile(user_id)
    return user['is_admin']



class edit_dish_categoy(StatesGroup):
    get_new_category = State()

class edit_dish_name(StatesGroup):
    get_new_name = State()

class edit_dish_caption(StatesGroup):
    get_new_caption = State()

class edit_dish_price(StatesGroup):
    get_new_price = State()

class edit_dish_photo(StatesGroup):
    get_new_photo = State()




@router.message(F.text == "✏️ Изменить")
@router.message(Command("edit"))
async def show_edit_dishes(message: Message):

    if not is_admin_user(message.from_user.id):
        await message.answer("⛔ Это действие доступно только администратору.")
        return 


    buttons = await get_dishes_edit_btn()



    if len(buttons.inline_keyboard) < 1:
        await message.answer("В списке пока нет блюд")
        return

    await message.answer("Выберите блюдо которого хотите изменить", reply_markup= buttons )



@router.callback_query(F.data.startswith("dishe_"))
async def dish_edit_options(callback: CallbackQuery, state: FSMContext):

    dish_id = callback.data.split("_")[1]
    photo = await get_photo(dish_id)
    dish = await about_dish(dish_id)
    
    if photo and photo['photo_file_id']:
        await callback.message.answer_photo(photo=photo['photo_file_id']) 

    text = (f"🍽 {dish['name']}\n\n"
        f"  Категория: {dish['category']}\n\n"
        f"💰 Цена: {dish['price']}\n"
        f"📝 Описание: {dish['caption'] or 'Нет описания'}")
    
        
    await callback.message.answer(text)
    await state.update_data(dish_id = dish_id)

    await callback.message.answer("Выберите опцию ", reply_markup= await get_edit_options())
    await callback.answer()


@router.callback_query(F.data.startswith("edit_"))
async def get_edit_type(callback : CallbackQuery, state: FSMContext):

    option = callback.data.split("_")[1]

    if option == "ct":
        await callback.message.answer("Выберите новую категорию", reply_markup= await get_edit_categoires())
        await state.set_state(edit_dish_categoy.get_new_category)

    elif option == "name":
        await callback.message.answer("Введите новую имю для блюдо")
        await state.set_state(edit_dish_name.get_new_name)
    elif option == "caption":
        await callback.message.answer("Введите новую описание для блюдо")
        await state.set_state(edit_dish_caption.get_new_caption)
    elif option == "price":
        await callback.message.answer("Введите новую цену для блюдо")
        await state.set_state(edit_dish_price.get_new_price)
    elif option == "photo":
        await callback.message.answer("отправьте новую фото")
        await state.set_state(edit_dish_photo.get_new_photo)


    await callback.answer()






@router.callback_query(edit_dish_categoy.get_new_category, F.data.startswith("categorye_"))
async def get_new_ct_edit(callback: CallbackQuery, state: FSMContext):

    ct = callback.data.split("_")[1]
    data = await state.get_data()

    if await edit_dish_category_service(ct, data['dish_id']):
        await callback.answer.message("✅ Категория успешно обнавлен")
    else:
        await callback.message.answer("⚠️ Не удалось обновить категория блюдо. Попробуйте позже.")

    await state.clear()
    await callback.answer()



@router.message(edit_dish_name.get_new_name)
async def get_new_name_edit(message: Message, state: FSMContext):

    name = message.text
    await state.update_data(name = name)
    data =  await state.get_data()

    if await edit_dish_name_service(name, data['dish_id']):
        await message.answer("✅ Имя успешно обновлен")
    else:
        await message.answer("⚠️ Не удалось обновить имя блюдо. Попробуйте позже.")

    await state.clear()



@router.message(edit_dish_price.get_new_price)
async def get_new_name_edit(message: Message, state: FSMContext):

    price = message.text
    await state.update_data(price = price)
    data =  await state.get_data()
    if not price.isdigit():
        await message.answer("⚠️ Цена должен быть числом!")
    try:
        price = float(message.text.replace(',', '.'))
        if price <= 0:
            raise ValueError
    except ValueError:
        await message.answer("⚠️ Введите корректную цену (например: 25.50 или 25)")
        return

    if await edit_dish_price_service(price, data['dish_id']):
        await message.answer("✅ Цена  успешно обновлен")
    else:
        await message.answer("⚠️ Не удалось обновить цена блюдо. Попробуйте позже.")

    await state.clear()




@router.message(edit_dish_caption.get_new_caption)
async def get_new_caption_edit(message: Message, state: FSMContext):

    caption = message.text
    await state.update_data(caption = caption)
    data =  await state.get_data()

    if await edit_dish_caption_service(caption, data['dish_id']):
        await message.answer("✅ Описание успешно обновлен")
    else:
        await message.answer("⚠️ Не удалось обновить описание блюдо. Попробуйте позже.")

    await state.clear()





@router.message(edit_dish_photo.get_new_photo)
async def get_new_photo_edit(message: Message, state: FSMContext):

    if not message.photo:
        await message.answer("⚠️ Пожалуйста, отправьте именно фотографию.")
        return

    data = await state.get_data()

    success = await edit_dish_photo_service(message.photo[-1].file_id, data['dish_id'])
    await state.clear()

    if success:
        await message.answer("✅ Фотография блюдо успешно обнавлен!")
    else:
        await message.answer("⚠️ Не удалось обновить фотография блюдо. Попробуйте позже.")










@router.message(F.text == "Добавить категорию")
async def add_ct(message: Message, state: FSMContext):

    if not is_admin_user(message.from_user.id):
        await message.answer("⛔ Это действие доступно только администратору.")
        await state.clear()
        return 


    await message.answer("Введите имя новой категории")
    await state.set_state(add_category.get_name)


@router.message(add_category.get_name)
async def add_ct_get_name(message: Message, state: FSMContext):

    name = message.text

    if name == 'cls':
        await message.answer("Добавление категории отменено")
        await state.clear()
        return

    if not name or not name.strip():
        await message.answer("Имя категории не может быть пустым. Повторите попытку")
        return

    if await add_new_ct(name):
        await message.answer("✅ Категория успешно добавлено")
    else:
        await message.answer("⚠️ Не удалось добавить категорию. Попробуйте позже.")

    await state.clear()







@router.callback_query(F.data == "cancel")
async def cancel_action(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("↩️ Действие отменено.")
    await callback.answer("Отменено")





@router.message(Command("cancel"))
@router.message(F.text == "❌ Отмена")
async def cancel_by_message(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("↩️ Действие отменено.")


@router.message(F.text == "➕ Добавить блюдо")
@router.message(Command("add"))
async def new_dish(message: Message, state: FSMContext):

    if not await is_admin_user(message.from_user.id):
        await message.answer("⛔ Это действие доступно только администратору.")
        await state.clear()
        return

    
    category = await get_new_dish_ct()


    if len(category.inline_keyboard) < 1:
        await message.answer("⚠️ Сначала добавьте категории в базу данных.")
        await state.clear()
        return

    
    await message.answer("📂 Выберите категорию блюда:", reply_markup=category)
    await state.set_state(add_new_dish.get_dish_category)



@router.callback_query(add_new_dish.get_dish_category, F.data.startswith("dishct_"))
async def add_new_dish_ct(callback: CallbackQuery, state: FSMContext):

    if not await is_admin_user(callback.from_user.id):
        await callback.message.answer("⛔ Это действие доступно только администратору.")
        await state.clear()
        return
    
    ct = callback.data.split("_", 1)[1]

    await state.update_data(category=int(ct))

    await state.set_state(add_new_dish.get_dish_name)
    await callback.message.answer("✏️ Введите название блюда:", reply_markup=cancel_kb)
    await callback.answer()






@router.message(add_new_dish.get_dish_name)
async def add_new_dish_name(message: Message, state: FSMContext):

    if not message.text or not message.text.strip():
        await message.answer("⚠️ Название не должно быть пустым. Попробуйте ещё раз.")
        return
    
    await state.update_data(name = message.text.strip())
    await message.answer("📝 Введите описание блюда или отправьте 0, чтобы пропустить:", reply_markup=cancel_kb)

    await state.set_state(add_new_dish.get_dish_caption)




@router.message(add_new_dish.get_dish_caption)
async def add_new_dish_caption(message: Message, state: FSMContext):

    if not message.text:
        await message.answer("⚠️ Отправьте текст или 0, чтобы пропустить.")
        return
    
    caption = "" if message.text.strip() == "0" else message.text.strip()

    await state.update_data(caption = caption)

    await message.answer("💰 Введите цену блюда (например, 25 или 25.50):", reply_markup=cancel_kb)
    await state.set_state(add_new_dish.get_dish_price)






@router.message(add_new_dish.get_dish_price)
async def add_new_dish_price(message: Message, state: FSMContext):


    if not message.text:
        await message.answer("⚠️ Введите цену числом.")
        return
    
    try:
        price = float(message.text.replace(',', '.'))
        if price <= 0:
            raise ValueError
    except ValueError:
        await message.answer("⚠️ Введите корректную цену (например: 25.50)")
        return
    
    await state.update_data(price=str(price))
    await message.answer("📷 Отправьте фотографию блюда:", reply_markup=cancel_kb)
    await state.set_state(add_new_dish.get_dish_photo)



@router.message(add_new_dish.get_dish_photo)
async def add_new_dish_photo(message: Message, state: FSMContext):


    if not message.photo:
        await message.answer("⚠️ Пожалуйста, отправьте именно фотографию.", reply_markup=cancel_kb)
        return

    
    data = await state.get_data()

    success = await dish_add(data['category'], data['name'], data['caption'], data['price'], message.photo[-1].file_id)
    await state.clear()

    if success:
        await message.answer("✅ Блюдо успешно добавлено!")
    else:
        await message.answer("⚠️ Не удалось добавить блюдо. Попробуйте позже.")



@router.message(F.text == "🗑 Удалить блюдо")
@router.message(Command("del"))
async def delete(message: Message, state: FSMContext):

    if not is_admin_user(message.from_user.id):
        await message.answer("⛔ Это действие доступно только администратору.")
        await state.clear()
        return 


    buttons = await get_dishes_all_btn()

    if len(buttons.inline_keyboard) < 1:
        await message.answer("📭 В меню пока нет блюд.")
        return
        await state.clear()

    
    await message.answer("🗑 Выберите блюдо, которое хотите удалить:", reply_markup=buttons)
    await state.set_state(delete_dish.get_dish_id)



@router.callback_query(delete_dish.get_dish_id, F.data.startswith("dishd_"))
async def choose_dish_to_delete(callback: CallbackQuery, state: FSMContext):


    if not is_admin_user(callback.from_user.id):
        await callback.message.answer("⛔ Это действие доступно только администратору.")
        await state.clear()
        return
    
    dish_id = int(callback.data.split("_", 1)[1])

    dish = await about_dish(dish_id)


    if not dish:
        await callback.message.answer("⚠️ Это блюдо уже недоступно.")
        await state.clear()
        await callback.answer()
        return

    
    await state.update_data(delete_dish_id=dish_id)

    buttons = await get_delete_confirm_btn(dish_id)
    await callback.message.answer(f"Вы действительно хотите удалить блюдо «{dish['name']}»?", reply_markup = buttons)
    await callback.answer()





@router.callback_query(F.data.startswith("confirm_delete_"))
async def confirm_delete(callback: CallbackQuery, state: FSMContext):


    if not is_admin_user(callback.from_user.id):
        await callback.message.answer("⛔ Это действие доступно только администратору.")
        await state.clear()
        return

    
    dish_id = callback.data.rsplit("_", 1)[1]
    result = await delete_dishs(dish_id)

    if await delete_dishs(dish_id):
        await callback.message.answer("✅ Блюдо успешно удалено.")
    else:
        await callback.message.answer("⚠️ Не удалось удалить блюдо. Возможно, оно уже удалено или используется в заказах.")

    await state.clear()
    await callback.answer()



@router.message(F.text == "📋 Список блюд")
@router.message(Command("dishes"))
async def list_dishes(message: Message):

    if not await is_admin_user(message.from_user.id):
        await message.answer("⛔ Это действие доступно только администратору.")
        return
    
    dishes = await get_all_dishes()

    if not dishes:
        await message.answer("📭 В меню пока нет блюд.")
        return
    
    text = ["📋 **Список блюд:**"]


    for dish in dishes:
        text.append(f"• {dish['name']} — {dish['price']}\n  Категория: {dish['category_name'] or 'не указана'}")


    await message.answer("\n".join(text), parse_mode="Markdown")



@router.callback_query(F.data == "back_categories")
async def back_categories(callback: CallbackQuery, state: FSMContext):

    await state.clear()

    categories = await get_category_btn()
    await callback.message.answer("🍽 Выберите категорию:", reply_markup=categories)

    await callback.answer()




@router.callback_query(F.data.startswith("category_"))
async def show_dishes(callback: CallbackQuery):


    category_id = callback.data.split("_", 1)[1]
    dishes = await get_ct_dishes_btn(category_id)

    if len(dishes.inline_keyboard) < 1:
        await callback.answer("В этой категории пока нет блюд.")
        return

    
    await callback.message.answer("🍽 Выберите блюдо:", reply_markup=dishes)
    await callback.answer()

@router.callback_query(F.data.startswith("dish_"))
async def show_dish(callback: CallbackQuery, state: FSMContext):

    dish_id = callback.data.split("_", 1)[1]
    
    dish = await about_dish(dish_id)
    
    
    if not dish:
        await callback.answer("Блюдо не найдено.")
        return

    
    await state.clear()
    await state.update_data(dish_id=int(dish_id))


    photo = await get_photo(dish_id)


    if photo and photo['photo_file_id']:
        await callback.message.answer_photo(photo=photo['photo_file_id'])

    text = (f"🍽 <b>{dish['name']}</b>\n\n"
            f"💰 Цена: {dish['price']}\n"
            f"📝 Описание: {dish['caption'] or 'Нет описания'}")

    
    await callback.message.answer(text, reply_markup = await get_order_btn(), parse_mode="HTML")


    await callback.answer()




@router.callback_query(F.data == "new_order")
async def take_order(callback: CallbackQuery, state: FSMContext):


    data = await state.get_data()
    
    if not data.get('dish_id'):
        await callback.answer("Сначала выберите блюдо.", show_alert=True)
        return
    
    await state.set_state(get_order.get_order_count)

    await callback.message.answer("🔢 Введите количество:", reply_markup=cancel_kb)

    await callback.answer()




@router.message(get_order.get_order_count)

async def get_order_count(message: Message, state: FSMContext):

    if not message.text or not message.text.isdigit() or int(message.text) <= 0:
        await message.answer("⚠️ Количество должно быть положительным целым числом. Попробуйте ещё раз.", reply_markup=cancel_kb)
        return


    
    await state.update_data(quantity=int(message.text))

    await message.answer("🪑 Введите номер столика:", reply_markup=cancel_kb)

    await state.set_state(get_order.get_order_table)






@router.message(get_order.get_order_table)
async def get_order_table(message: Message, state: FSMContext):

    if not message.text or not message.text.isdigit() or int(message.text) <= 0:
        await message.answer("⚠️ Номер столика должен быть положительным целым числом. Попробуйте ещё раз.", reply_markup=cancel_kb)
        return
    
    await state.update_data(table=int(message.text))

    await message.answer("👤 Введите имя заказчика:", reply_markup=cancel_kb)
    await state.set_state(get_order.get_order_name)




@router.message(get_order.get_order_name)
async def get_order_name(message: Message, state: FSMContext):

    if not message.text or not message.text.strip():
        await message.answer("⚠️ Имя не должно быть пустым. Попробуйте ещё раз.", reply_markup=cancel_kb)
        return

    
    await state.update_data(name = message.text.strip())

    data = await state.get_data()
    dish = await about_dish(data['dish_id'])

    result = await take_new_order(message.from_user.id, data['dish_id'], data['quantity'], data['table'], data['name'])

    await state.clear()

    if result:

        dish_name = dish['name'] if dish else 'Блюдо'
        await message.answer(f"✅ Заказ успешно оформлен!\n\n🍽 Блюдо: {dish_name}\n🔢 Количество: {data['quantity']}\n🪑 Столик: {data['table']}\n👤 Имя: {data['name']}")
    else:
        await message.answer("⚠️ Не удалось оформить заказ. Попробуйте ещё раз.")



@router.message(F.text == "🔐 Войти как администратор")
@router.message(Command("login"))
async def login(message: Message, state: FSMContext):
    user = await profile(message.from_user.id)
    if user["is_admin"]:
        await message.answer("🛠 У вас уже есть права администратора!")
        return
    await message.answer("🔐 Введите пароль администратора для получения прав:")
    await state.set_state(Login.password)





@router.message(Login.password)
async def login_admin(message: Message, state: FSMContext):
    user = await profile(message.from_user.id)
    password = message.text
    if message.text == 'cls':
        await state.clear()
        await message.answer("↩️ Вход отменён.")
        return

    if password != user["password"]:
        await message.answer("❌ Неверный пароль администратора.")
        await state.clear()
        return

    if await become_admin(message.from_user.id):
        await message.answer("""
Добро пожаловать! 😏
🛠 Теперь тебе доступны инструменты управления Меню.
""", reply_markup=admin_kb)
        await state.clear()
        return
    else:
        await message.answer("⚠️ Не удалось выдать права администратора. Попробуйте позже.")
        await state.clear()