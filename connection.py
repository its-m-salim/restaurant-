import asyncpg
from dotenv import load_dotenv
import os


load_dotenv()

p_db = os.getenv("PASSWORD_DB")

async def connection_db():
    try:
        conn = await asyncpg.connect(
        host="localhost",
        port=5432,
        user="salim",
        database="restaurant",
        password= p_db
        )
        return conn
    except Exception as error:
        print(f"{type(error)}: {error} conn.py")



async def create_tables():
    try:
        conn = await connection_db()
        await conn.execute("""
        create table if not exists users(
            id serial primary key,
            telegram_id varchar(200) unique,
            full_name varchar(200),
            username varchar(200),
            password varchar(200),
            created_at timestamp default now(),
            is_admin bool default false,
            is_active bool default true

           );

        create table if not exists categories(
            id serial primary key,
            name varchar(200),
            created_at timestamp default now(),
            is_active bool default true
        );
        
        create table if not exists dishes(
            id serial primary key,
            category_id INTEGER REFERENCES categories(id) on delete cascade,
            name text not null,
            caption text,
            price numeric not null,
            photo_file_id text,
            is_active bool default true
        );

        CREATE Table if NOT exists orders(
            id SERIAL PRIMARY KEY,
            telegram_id varchar(200) not NULL,
            dish_id INT REFERENCES dishes(id) on delete cascade,
            quantity INT NOT NULL,
            table_number INT NOT NULL,
            customer_name text not null,
            created_at TIMESTAMP DEFAULT now()
);

""")
        print("tables created successfuly")
    except Exception as error:
        print(f"{type(error)}: {error} con.py")     
    finally:
        await conn.close()   