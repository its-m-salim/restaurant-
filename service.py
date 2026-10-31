from connection import *

async def create_user(username, full_name, tg_id):
    try:
        conn = await connection_db()
        await conn.execute("""
        INSERT INTO users(username, full_name, telegram_id) VALUES 
        ($1, $2, $3) 

        """, username, full_name, str(tg_id))
        return True
    
    except Exception as error:
        print(f"{type(error).__name__}: {error} create_user")
        return False
    finally:
        await conn.close()





async def get_all_dishes():
    try:
        conn = await connection_db()
        return await conn.fetch("""
        SELECT d.*, c.name AS category_name FROM dishes d 
        LEFT JOIN categories c ON c.id=d.category_id  
        ORDER BY d.id""")

        return True
    except Exception as error:
        print(f"{type(error).__name__}: {error} get_all_dishes")
        return False
    finally:
        await conn.close()

async def delete_dishs(b_id):
    try:
        conn = await connection_db()
        return await conn.fetchrow("""
        delete from  dishes WHERE id=$1 
        RETURNING id
        
        """, int(b_id))
    
    except Exception as error:
        print(f"{type(error).__name__}: {error} delete_dishs")
        return False
    finally:
        await conn.close()



async def profile(tg_id):

    try:
        conn = await connection_db()
        user =  await conn.fetchrow("""
        
        SELECT * FROM users 
        WHERE telegram_id=$1 
        """, str(tg_id))

        return user
    
    except Exception as error:
        print(f"{type(error).__name__}: {error} profile")
        return False
    finally:
        await conn.close()



async def about_dish(dish_id):
    try:
        conn = await connection_db()
        dish =  await conn.fetchrow("""
        
        select dishes.name, dishes.price, dishes.caption, categories.name as category from dishes
        join categories on categories.id = dishes.category_id 
        where dishes.id=$1 
        
        """, int(dish_id))

        return dish
    except Exception as error:
        print(f"{type(error).__name__}: {error} about_dish")
        return False
    finally:
        await conn.close()




async def get_categories():
    try:
        conn = await connection_db()
        ct =  await conn.fetch("""
        
        SELECT * FROM categories 
        ORDER BY id""")

        return ct
    except Exception as error:
        print(f"{type(error).__name__}: {error} get_categories")
        return False
    finally:
        await conn.close()



async def become_admin(tg_id):
    try:
        conn = await connection_db()
        result = await conn.fetchrow("""
        
        update users 
        set is_admin=true 
        where telegram_id=$1 RETURNING id
        """, str(tg_id))


        if not result:
            return False

        return True
    except Exception as error:
        print(f"{type(error).__name__}: {error} become_admin")
        return False
    finally:
        await conn.close()



async def set_password(password, tg_id):
    try:
        conn = await connection_db()
        await conn.execute("""

        UPDATE users 
        SET password=$1 
        WHERE telegram_id=$2

        """, password, str(tg_id))

        return True
    except Exception as error:
        print(f"{type(error).__name__}: {error} set_password")
        return False
    finally:
        await conn.close()




async def get_category_dishes(category_id):
    try:
        conn = await connection_db()
        dishes =  await conn.fetch("""
        
        SELECT * FROM dishes 
        WHERE category_id=$1 
        ORDER BY id
        """, int(category_id))

        return dishes
    except Exception as error:
        print(f"{type(error).__name__}: {error} get_category_dishes")
        return False
    finally:
        await conn.close()



async def take_new_order(tg_id, dish_id, quantity, table_n, customer_name):
    try:
        conn = await connection_db()
        result = await conn.fetchrow("""
        insert INTO orders(telegram_id,dish_id,quantity,table_number,customer_name) values
         ($1, $2, $3, $4, $5) 
         returning  id
         """, str(tg_id), int(dish_id), int(quantity), int(table_n), customer_name)

        if not result:
            return False

        return True
    except Exception as error:
        print(f"{type(error).__name__}: {error} take_new_order")
        return False
    finally:
        await conn.close()



async def save_photo(dish_id, file_id):
    try:
        conn = await connection_db()
        result = await conn.fetchrow("""
        
        UPDATE dishes 
        SET photo_file_id=$1 
        WHERE id=$2 RETURNING id

""", file_id, int(dish_id))

        if not result:
            return False

        return True
    except Exception as error:
        print(f"{type(error).__name__}: {error} save_photo")
        return False
    finally:
        await conn.close()



async def get_photo(dish_id):
    try:
        conn = await connection_db()
        return await conn.fetchrow("""
        
        SELECT photo_file_id FROM dishes 
        WHERE id=$1 
        
""", int(dish_id))
    
    except Exception as error:
        print(f"{type(error).__name__}: {error} get_photo")
        return False
    finally:
        await conn.close()



async def dish_add(ct_id, name, caption, price, photo):
    try:
        conn = await connection_db()
        result = await conn.fetchrow("""
        insert into dishes(category_id, name, caption, price, photo_file_id) values
            ($1, $2, $3, $4, $5) 
            
        returning id
""", int(ct_id), name, caption, float(price), photo)

        if not result:
            return False

        return True
    except Exception as error:
        print(f"{type(error).__name__}: {error} dish_add")
        return False
    finally:
        await conn.close()



async def g_orders():
    try:
        conn = await connection_db()
        orders =  await conn.fetch("""
        select * , dishes.name as dish from orders
        join dishes on dishes.id = orders.dish_id
        """)

        return orders
    except Exception as error:
        print(f"{type(error).__name__}: {error} get_category_dishes")
        return False
    finally:
        await conn.close()





async def add_new_ct(name):
    try:
        conn = await connection_db()
        await conn.execute("""
    insert into categories(name) values
    ($1)
""", name)
        return True
    except Exception as error:
        print(f"{type(error)}: {error} sac.py")  
        return False   
    finally:
        await conn.close()   




async def edit_dish_category_service(ct_id, dish_id):
    try:
        conn =await connection_db()
        result = await conn.fetchrow("""
        update dishes
        set category_id = $1
        where id = $2
        returning id
""", int(ct_id), int(dish_id))

        if not result:
            return False

        return True
    except Exception as error:
        print(f"{type(error)}: {error} sedc.py")     
        return False
    finally:
        await conn.close()   




async def edit_dish_name_service(name, dish_id):
    try:
        conn =await connection_db()
        result = await conn.fetchrow("""
        update dishes
        set name = $1
        where id = $2
        returning id
""", name , int(dish_id))

        if not result:
            return False

        return True
    except Exception as error:
        print(f"{type(error)}: {error} sedn.py")     
        return False
    finally:
        await conn.close()   



async def edit_dish_caption_service(caption, dish_id):
    try:
        conn =await connection_db()
        result = await conn.fetchrow("""
        update dishes
        set caption = $1
        where id = $2
        returning id
""", caption , int(dish_id))

        if not result:
            return False

        return True
    except Exception as error:
        print(f"{type(error)}: {error} sedc.py")     
        return False
    finally:
        await conn.close()   



async def edit_dish_price_service(price, dish_id):
    try:
        conn =await connection_db()
        result = await conn.fetchrow("""
        update dishes
        set price = $1
        where id = $2
        returning id
""", float(price) , int(dish_id))

        if not result:
            return False

        return True
    except Exception as error:
        print(f"{type(error)}: {error} sedp.py")     
        return False
    finally:
        await conn.close()   


async def edit_dish_photo_service(photo, dish_id):
    try:
        conn =await connection_db()
        result = await conn.fetchrow("""
        update dishes
        set photo_file_id = $1
        where id = $2
        returning id
""",str(photo), int(dish_id))

        if not result:
            return False

        return True
    except Exception as error:
        print(f"{type(error)}: {error} sedp.py")     
        return False
    finally:
        await conn.close()   

        