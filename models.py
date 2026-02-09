from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from datetime import date

db = SQLAlchemy()

class UserRole(Enum):
    STUDENT = 'ученик'
    ADMIN = 'администратор'
    COOK = 'повар'


class MealType(Enum):
    BREAKFAST = 'завтрак'
    LUNCH = 'обед'


class Unit(Enum):
    LITERS = 'л.'
    GRAMMS = 'г.'
    KILOGRAMMS = 'кг.'
    UNITS = 'шт.'

class FoodType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(255))

    role = db.Column(db.Enum(UserRole), default=UserRole.STUDENT)
    money = db.Column(db.Integer)


class PaidMenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    is_taken = db.Column(db.Boolean, default=False)


class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True, nullable=False)
    amount = db.Column(db.Float)
    unit = db.Column(db.Enum(Unit))


class Compound(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    amount = db.Column(db.Float)


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    type = db.Column(db.Enum(MealType))


class MenuDishes(db.Model):
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), primary_key=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True, nullable=False)
    unit = db.Column(db.Enum(Unit))
    amount = db.Column(db.Float)


class ProductType(db.Model):
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('food_type.id'), primary_key=True)


class AllergyProducts(db.Model):
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    allergy_id = db.Column(db.Integer, db.ForeignKey('allergy.id'), primary_key=True)


class Allergy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True, nullable=False)
    description = db.Column(db.String(500))


class UserDisliked(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('food_type.id'), primary_key=True)


class UserAllergy(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    allergy_id = db.Column(db.Integer, db.ForeignKey('allergy.id'), primary_key=True)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'))


class ProductRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    amount = db.Column(db.Float)
    is_agreed = db.Column(db.Boolean, default=False)
    created = db.Column(db.Date, default=date.today)
    fulfilled = db.Column(db.Date)
