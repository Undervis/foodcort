import random
import sqlite3

sql = sqlite3.connect("db.sqlite3")
cursor = sql.cursor()

cursor.execute("create table if not exists Dish("
               "id integer primary key autoincrement, description text, "
               "category varchar(32), name varchar(32), price float, img text)")
cursor.execute("create table if not exists User("
               "id integer primary key autoincrement, login varchar(32), email varchar(32), phone varchar(16), "
               "password varchar(32), img text nullable, token int)")
cursor.execute('create table if not exists Cart('
               'id integer primary key autoincrement, user_token references User(token), '
               'dish_id int references Dish(id))')
sql.commit()


def get_dishes():
    cursor.execute("select * from Dish")
    return cursor.fetchall()


def add_dish(category, name, price, img, description):
    if not len(cursor.execute(f'select * from Dish where name="{name}" or description="{description}"').fetchall()) > 0:
        cursor.execute(f'insert into Dish (category, name, price, img, description)'
                       f' values ("{category}", "{name}", {price}, "{img}", "{description}")')
        sql.commit()
        return 0
    else:
        return 2


def add_to_cart(token, dish_id):
    cursor.execute(f'insert into Cart (user_token, dish_id) values ({token}, {dish_id})')
    sql.commit()


def get_cart(token):
    return cursor.execute(f"select * from Cart where user_token={token}").fetchall()


def delete_from_cart(cart_item_id, user_token):
    cursor.execute(f'delete from Cart where id={cart_item_id} and user_token={user_token}')
    sql.commit()


def delete_dish(dish_id):
    cursor.execute(f"delete from Dish where id = {dish_id}")
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
