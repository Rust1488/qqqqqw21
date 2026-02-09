from datetime import date as _date
from datetime import datetime

from flask import Blueprint, jsonify, request

from models import db, Menu, MenuDishes, Dish


menu_bp = Blueprint("menu", __name__, url_prefix="/menu")


def _dish_to_dict(d: Dish) -> dict:
    return {
        "id": d.id,
        "name": d.name,
        "amount": d.amount,
        "unit": (d.unit.value if d.unit else None),
        "unit_code": (d.unit.name if d.unit else None),
    }


def _menu_to_dict(m: Menu) -> dict:
    dishes = (
        db.session.query(Dish)
        .join(MenuDishes, MenuDishes.dish_id == Dish.id)
        .filter(MenuDishes.menu_id == m.id)
        .order_by(Dish.name.asc())
        .all()
    )

    return {
        "id": m.id,
        "date": m.date.isoformat() if m.date else None,
        "type": (m.type.value if m.type else None),
        "type_code": (m.type.name if m.type else None),
        "dishes": [_dish_to_dict(d) for d in dishes],
    }


def _parse_date(date_str: str) -> _date | None:
    try:
        return _date.fromisoformat(date_str)
    except Exception:
        return None


@menu_bp.get("/today")
def menu_today():
    today = _date.today()
    menus = Menu.query.filter_by(date=today).order_by(Menu.id.asc()).all()

    return jsonify({
        "date": today.isoformat(),
        "menus": [_menu_to_dict(m) for m in menus],
    })


@menu_bp.get("")
def menu_by_date_query():
    date_str = (request.args.get("date") or "").strip()
    if not date_str:
        return jsonify({"message": "Нужен параметр date в формате YYYY-MM-DD"}), 400

    d = _parse_date(date_str)
    if not d:
        return jsonify({"message": "Неверный формат date. Используй YYYY-MM-DD"}), 400

    menus = Menu.query.filter_by(date=d).order_by(Menu.id.asc()).all()
    return jsonify({
        "date": d.isoformat(),
        "menus": [_menu_to_dict(m) for m in menus],
    })


@menu_bp.get("/<date_str>")
def menu_by_date_path(date_str: str):
    d = _parse_date(date_str.strip())
    if not d:
        return jsonify({"message": "Неверный формат даты. Используй YYYY-MM-DD"}), 400

    menus = Menu.query.filter_by(date=d).order_by(Menu.id.asc()).all()
    return jsonify({
        "date": d.isoformat(),
        "menus": [_menu_to_dict(m) for m in menus],
    })
