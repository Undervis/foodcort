from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from models import *
import db

tags_meta = [
    {
        "name": "Dishes",
        "description": "Функции для взаимодействия с блюдами"
    },
    {
        "name": "Auth",
        "description": "Функции для авторизации пользователя(вход и регистрация)"
    },
    {
        "name": "Cart",
        "description": "Функции для взаимодействия с корзиной"
    }
]

app = FastAPI(
    title="Food delivery API",
    version="1.0",
    contact={
        "name": "Всесоздатель",
        "url": "https://vk.com/theundervis",
        "email": "k.lychkovsky.undervis@gmail.com"
    }, openapi_tags=tags_meta
)


@app.get("/", description="Для теста API")
async def root():
    return {"message": "Ну чо могу сказать, апи работает"}


@app.post("/add_dish", description="Для добавления нового блюда", tags=['Dishes'])
async def add_dish_request(dish: Dish):
    try:
        db.add_dish(name=dish.name, category=dish.category, price=dish.price, img=dish.img,
                    description=dish.description)
        return {"message": "Блюдо добавлено"}
    except:
        raise HTTPException(status_code=400, detail={"message": "Что-то пошло не так"})


@app.get('/dishes', description="Вывод списка блюд", tags=['Dishes'])
async def get_dishes_request():
    dishes = []
    for dish in db.get_dishes():
        dishes.append({"id": dish[0], "name": dish[3], "category": dish[2], "description": dish[1],
                       "price": dish[4], 'img_url': dish[5]})
    return dishes


@app.get("/get_dish/{dish_id}", description="Получение блюда по его id", tags=['Dishes'])
async def get_dish_request(dish_id: int):
    dish = db.get_dish(dish_id)
    if dish:
        dish = {"id": dish[0], "name": dish[3], "category": dish[2], "description": dish[1],
                "price": dish[4], 'img_url': dish[5]}
        return dish
    else:
        raise HTTPException(status_code=400, detail={"message": "Такого блюда не нашлось"})


@app.delete("/delete_dish/{dish_id}", description="Удаление блюда по его id", tags=['Dishes'])
async def delete_dish_request(dish_id: int):
    db.delete_dish(dish_id)
    return {"message": "Блюдо съели", "error": 0}


@app.post("/auth/register", description="Регистрация нового пользователя", tags=["Auth"])
async def auth_register_request(user: UserRegister):
    if db.auth_register(user.email, user.login, user.password, user.phone):
        return {"message": "Пользователь успешно зарегистрирован", "token": db.auth_login(user.email, user.password)[0]}
    else:
        raise HTTPException(status_code=400, detail={"message": "Пользователь с таким логином или почтой уже есть"})


@app.post("/auth/login", description="Авторизация зарегистрированного пользователя", tags=["Auth"])
async def auth_login_request(user: UserLogin):
    token = db.auth_login(user.email, user.password)
    if token:
        return {"message": "Успешная авторизация", "token": token[0]}
    else:
        raise HTTPException(status_code=400, detail={"message": "Неверный логин или пароль"})


@app.post("/add_to_cart", description="Добавление блюда в корзину пользователя", tags=["Cart"])
async def add_to_cart_request(user_token: int, dish_id: int):
    try:
        db.add_to_cart(user_token, dish_id)
        return {"message": "Блюдо добавлено в корзину"}
    except:
        raise HTTPException(status_code=400, detail={"message": "Что-то пошло не так"})


@app.get("/get_cart/{token}", description="Получение корзины пользователя", tags=["Cart"])
async def get_cart_request(token: int):
    cart = []
    for item in db.get_cart(token):
        dish = db.get_dish(item[2])
        cart.append({"id": item[0], "token": item[1], "dish_id": dish[0], "name": dish[3], "category": dish[2],
                     "description": dish[1],
                     "price": dish[4], 'img_url': dish[5]})
    return cart


@app.delete("/delete_from_cart", description="Удаление блюда из корзины пользователя", tags=["Cart"])
async def delete_from_cart_request(item_id: int, user_token: int):
    db.delete_from_cart(item_id, user_token)
    return {"message": "Блюдо удалено из корзины"}


@app.post("/add_to_order", description="Перенос корзины в заказ", tags=["Cart"])
async def add_to_order(user_token: int, cart_ids: list):
    db.add_to_order(user_token, cart_ids)
    return {"message": "Блюда перенесены в заказ"}
