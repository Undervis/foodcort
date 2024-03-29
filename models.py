from pydantic import BaseModel


class Dish(BaseModel):
    category: str
    name: str
    price: float
    img: str
    description: str


class UserRegister(BaseModel):
    login: str
    email: str
    phone: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class Order(BaseModel):
    token: int
    cart_ids: list
