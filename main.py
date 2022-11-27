from fastapi import FastAPI, HTTPException
from models import *
import db

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Ну чо могу сказать, апи работает"}


@app.post("/add_dish", status_code=200)
async def add_dish_request(dish: Dish):
    if db.add_dish(name=dish.name, category=dish.category, price=dish.price, img=dish.img,
                   description=dish.description):
        return {"message": "Всё пучком", "error": 0}
    else:
        raise HTTPException(status_code=400, detail={"message": "Хана, не добавилось, проверяй параметры", "error": 1})


@app.get('/dishes')
async def get_dishes_request():
    dishes = []
    for dish in db.get_dishes():
        dishes.append({"id": dish[0], "name": dish[3], "category": dish[2], "description": dish[1],
                       "price": dish[4], 'img_url': dish[5]})
    return dishes


@app.get("/get_dish/{dish_id}")
async def get_dish_request(dish_id: int):
    dish = db.get_dish(dish_id)
    if dish:
        dish = {"id": dish[0], "name": dish[3], "category": dish[2], "description": dish[1],
                "price": dish[4], 'img_url': dish[5]}
        return dish
    else:
        raise HTTPException(status_code=400, detail={"message": "Такого блюда не нашлось"})


@app.delete("/delete_dish/{dish_id}")
async def delete_dish_request(dish_id: int):
    db.delete_dish(dish_id)
    return {"message": "Блюдо съели", "error": 0}


@app.post("/auth/register")
async def auth_register_request(user: UserRegister):
    if db.auth_register(user.email, user.login, user.password, user.phone):
        return {"message": "Пользователь успешно зарегистрирован", "token": db.auth_login(user.email, user.password)[0]}
    else:
        raise HTTPException(status_code=400, detail={"message": "Пользователь с таким логином или почтой уже есть"})


@app.post("/auth/login")
async def auth_login_request(user: UserLogin):
    token = db.auth_login(user.email, user.password)
    if token:
        return {"message": "Успешная авторизация", "token": token[0]}
    else:
        raise HTTPException(status_code=400, detail={"message": "Неверный логин или пароль"})
