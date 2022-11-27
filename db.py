import random
import sqlite3

sql = sqlite3.connect("db.sqlite3")
cursor = sql.cursor()

cursor.execute("create table if not exists Dish("
               "id integer primary key autoincrement, category varchar(32), name varchar(32), price float, img text)")
cursor.execute("create table if not exists User("
               "id integer primary key autoincrement, login varchar(32), email varchar(32), phone varchar(16), "
               "password varchar(32), img text nullable, token int)")
sql.commit()


def get_dishes():
    cursor.execute("select * from Dish")
    return cursor.fetchall()


def add_dish(category, name, price, img):
    cursor.execute(f'insert into Dish (category, name, price, img) values ("{category}", "{name}", {price}, "{img}")')
    sql.commit()
    return True


def delete_dish(dish_id):
    cursor.execute(f"delete from Dish where id={dish_id}")
    sql.commit()
    return True


def get_dish(dish_id):
    cursor.execute(f"select * from Dish where id = {dish_id}")
    return cursor.fetchone()


def auth_login(email, password):
    result = cursor.execute(f'select token from User where email="{email}" and password="{password}"').fetchone()
    return result


def auth_register(email, login, password, phone):
    users = cursor.execute(f'select * from User where login="{login}" or email="{email}"').fetchall()
    if len(users) > 0:
        return False
    else:
        cursor.execute(f'insert into User (email, login, password, phone, token) values ('
                       f'"{email}", "{login}", "{password}", "{phone}", {random.randrange(1000, 10000)})')
        sql.commit()
        return True
