from datetime import date, timedelta
from werkzeug.security import generate_password_hash

from models import (
    db,
    UserRole, MealType, Unit,
    User, FoodType, Product, ProductType,
    Allergy, AllergyProducts, UserDisliked, UserAllergy,
    Dish, Compound, Menu, MenuDishes,
    PaidMenu, Feedback, ProductRequest
)

def seed_test_data(start=date(2026, 2, 9), days=10):
    """
    Заполняет БД тестовыми данными на N дней, начиная с start.
    По умолчанию: 10 дней с 09.02.2026 по 18.02.2026 включительно.
    Чтобы получить по 19.02 включительно — поставь days=11.
    """
    # --- helpers ---
    def daterange(d0, n):
        for i in range(n):
            yield d0 + timedelta(days=i)

    # Очистка (по желанию). Если не нужно — закомментируй.
    # Важно: порядок удаления из-за FK.
    for model in [
        Feedback, PaidMenu, MenuDishes, Menu, Compound, Dish,
        ProductRequest, AllergyProducts, UserAllergy, UserDisliked,
        ProductType, Allergy, Product, FoodType, User
    ]:
        db.session.query(model).delete()

    # --- справочники ---
    food_types = [
        FoodType(name="Молочные"),
        FoodType(name="Мясо"),
        FoodType(name="Овощи"),
        FoodType(name="Фрукты"),
        FoodType(name="Крупы"),
        FoodType(name="Рыба"),
        FoodType(name="Выпечка"),
        FoodType(name="Напитки"),
    ]
    db.session.add_all(food_types)
    db.session.flush()

    ft = {x.name: x for x in food_types}

    products = [
        Product(name="Молоко", unit=Unit.LITERS, amount=50.0),
        Product(name="Кефир", unit=Unit.LITERS, amount=30.0),
        Product(name="Сыр", unit=Unit.KILOGRAMMS, amount=10.0),
        Product(name="Яйца", unit=Unit.UNITS, amount=200.0),
        Product(name="Мука", unit=Unit.KILOGRAMMS, amount=25.0),
        Product(name="Рис", unit=Unit.KILOGRAMMS, amount=20.0),
        Product(name="Гречка", unit=Unit.KILOGRAMMS, amount=20.0),
        Product(name="Курица", unit=Unit.KILOGRAMMS, amount=35.0),
        Product(name="Говядина", unit=Unit.KILOGRAMMS, amount=25.0),
        Product(name="Рыба (филе)", unit=Unit.KILOGRAMMS, amount=18.0),
        Product(name="Картофель", unit=Unit.KILOGRAMMS, amount=60.0),
        Product(name="Морковь", unit=Unit.KILOGRAMMS, amount=20.0),
        Product(name="Лук", unit=Unit.KILOGRAMMS, amount=20.0),
        Product(name="Помидоры", unit=Unit.KILOGRAMMS, amount=15.0),
        Product(name="Огурцы", unit=Unit.KILOGRAMMS, amount=15.0),
        Product(name="Яблоки", unit=Unit.KILOGRAMMS, amount=25.0),
        Product(name="Бананы", unit=Unit.KILOGRAMMS, amount=20.0),
        Product(name="Чай", unit=Unit.GRAMMS, amount=1000.0),
        Product(name="Сахар", unit=Unit.KILOGRAMMS, amount=15.0),
        Product(name="Соль", unit=Unit.KILOGRAMMS, amount=5.0),
        Product(name="Масло сливочное", unit=Unit.KILOGRAMMS, amount=8.0),
        Product(name="Масло растительное", unit=Unit.LITERS, amount=10.0),
        Product(name="Хлеб", unit=Unit.UNITS, amount=80.0),
    ]
    db.session.add_all(products)
    db.session.flush()
    pr = {p.name: p for p in products}

    # классификация продуктов по типам
    product_types_map = {
        "Молоко": ["Молочные", "Напитки"],
        "Кефир": ["Молочные", "Напитки"],
        "Сыр": ["Молочные"],
        "Яйца": ["Молочные"],  # условно
        "Мука": ["Крупы", "Выпечка"],
        "Рис": ["Крупы"],
        "Гречка": ["Крупы"],
        "Курица": ["Мясо"],
        "Говядина": ["Мясо"],
        "Рыба (филе)": ["Рыба"],
        "Картофель": ["Овощи"],
        "Морковь": ["Овощи"],
        "Лук": ["Овощи"],
        "Помидоры": ["Овощи"],
        "Огурцы": ["Овощи"],
        "Яблоки": ["Фрукты"],
        "Бананы": ["Фрукты"],
        "Чай": ["Напитки"],
        "Сахар": ["Крупы"],
        "Соль": ["Крупы"],
        "Масло сливочное": ["Молочные"],
        "Масло растительное": ["Крупы"],
        "Хлеб": ["Выпечка"],
    }
    pt_rows = []
    for pname, tnames in product_types_map.items():
        for tname in tnames:
            pt_rows.append(ProductType(product_id=pr[pname].id, type_id=ft[tname].id))
    db.session.add_all(pt_rows)

    # аллергии и привязки к продуктам
    allergies = [
        Allergy(name="Лактоза", description="Непереносимость молочных продуктов"),
        Allergy(name="Глютен", description="Непереносимость пшеницы/муки/хлеба"),
        Allergy(name="Рыба", description="Аллергия на рыбу"),
        Allergy(name="Яйца", description="Аллергия на яйца"),
    ]
    db.session.add_all(allergies)
    db.session.flush()
    al = {a.name: a for a in allergies}

    allergy_products = [
        AllergyProducts(product_id=pr["Молоко"].id, allergy_id=al["Лактоза"].id),
        AllergyProducts(product_id=pr["Кефир"].id, allergy_id=al["Лактоза"].id),
        AllergyProducts(product_id=pr["Сыр"].id, allergy_id=al["Лактоза"].id),
        AllergyProducts(product_id=pr["Мука"].id, allergy_id=al["Глютен"].id),
        AllergyProducts(product_id=pr["Хлеб"].id, allergy_id=al["Глютен"].id),
        AllergyProducts(product_id=pr["Рыба (филе)"].id, allergy_id=al["Рыба"].id),
        AllergyProducts(product_id=pr["Яйца"].id, allergy_id=al["Яйца"].id),
    ]
    db.session.add_all(allergy_products)

    # --- пользователи ---
    users = [
        User(login="admin@example.com", password_hash=generate_password_hash("hash_admin"), role=UserRole.ADMIN, money=0),
        User(login="cook@example.com", password_hash=generate_password_hash("hash_cook"), role=UserRole.COOK, money=0),
        User(login="student1@example.com", password_hash=generate_password_hash("hash_s1"), role=UserRole.STUDENT, money=3000),
        User(login="student2@example.com", password_hash=generate_password_hash("hash_s2"), role=UserRole.STUDENT, money=1500),
        User(login="student3@example.com", password_hash=generate_password_hash("hash_s3"), role=UserRole.STUDENT, money=500),
    ]
    db.session.add_all(users)
    db.session.flush()
    u = {x.login: x for x in users}

    # предпочтения/аллергии пользователей
    db.session.add_all([
        UserDisliked(user_id=u["student1@example.com"].id, type_id=ft["Рыба"].id),
        UserDisliked(user_id=u["student2@example.com"].id, type_id=ft["Молочные"].id),
        UserDisliked(user_id=u["student3@example.com"].id, type_id=ft["Овощи"].id),

        UserAllergy(user_id=u["student2@example.com"].id, allergy_id=al["Лактоза"].id),
        UserAllergy(user_id=u["student3@example.com"].id, allergy_id=al["Глютен"].id),
    ])

    # --- блюда ---
    dishes = [
        Dish(name="Овсяная каша на молоке", amount=250, unit=Unit.GRAMMS),
        Dish(name="Омлет", amount=180, unit=Unit.GRAMMS),
        Dish(name="Бутерброд с сыром", amount=120, unit=Unit.GRAMMS),
        Dish(name="Чай с сахаром", amount=250, unit=Unit.GRAMMS),

        Dish(name="Куриный суп", amount=300, unit=Unit.GRAMMS),
        Dish(name="Гречка с курицей", amount=320, unit=Unit.GRAMMS),
        Dish(name="Рис с говядиной", amount=320, unit=Unit.GRAMMS),
        Dish(name="Рыба с картофелем", amount=320, unit=Unit.GRAMMS),
        Dish(name="Овощной салат", amount=180, unit=Unit.GRAMMS),
        Dish(name="Фрукты (яблоко/банан)", amount=200, unit=Unit.GRAMMS),
    ]
    db.session.add_all(dishes)
    db.session.flush()
    d = {x.name: x for x in dishes}

    # состав блюд (Compound)
    compounds = [
        # завтрак
        Compound(dish_id=d["Овсяная каша на молоке"].id, product_id=pr["Молоко"].id, amount=0.25),
        Compound(dish_id=d["Овсяная каша на молоке"].id, product_id=pr["Сахар"].id, amount=0.01),
        Compound(dish_id=d["Омлет"].id, product_id=pr["Яйца"].id, amount=2),
        Compound(dish_id=d["Омлет"].id, product_id=pr["Молоко"].id, amount=0.05),
        Compound(dish_id=d["Бутерброд с сыром"].id, product_id=pr["Хлеб"].id, amount=1),
        Compound(dish_id=d["Бутерброд с сыром"].id, product_id=pr["Сыр"].id, amount=0.03),
        Compound(dish_id=d["Чай с сахаром"].id, product_id=pr["Чай"].id, amount=2),
        Compound(dish_id=d["Чай с сахаром"].id, product_id=pr["Сахар"].id, amount=0.01),

        # обед
        Compound(dish_id=d["Куриный суп"].id, product_id=pr["Курица"].id, amount=0.12),
        Compound(dish_id=d["Куриный суп"].id, product_id=pr["Картофель"].id, amount=0.10),
        Compound(dish_id=d["Куриный суп"].id, product_id=pr["Морковь"].id, amount=0.03),
        Compound(dish_id=d["Куриный суп"].id, product_id=pr["Лук"].id, amount=0.02),

        Compound(dish_id=d["Гречка с курицей"].id, product_id=pr["Гречка"].id, amount=0.10),
        Compound(dish_id=d["Гречка с курицей"].id, product_id=pr["Курица"].id, amount=0.12),

        Compound(dish_id=d["Рис с говядиной"].id, product_id=pr["Рис"].id, amount=0.10),
        Compound(dish_id=d["Рис с говядиной"].id, product_id=pr["Говядина"].id, amount=0.12),

        Compound(dish_id=d["Рыба с картофелем"].id, product_id=pr["Рыба (филе)"].id, amount=0.14),
        Compound(dish_id=d["Рыба с картофелем"].id, product_id=pr["Картофель"].id, amount=0.15),

        Compound(dish_id=d["Овощной салат"].id, product_id=pr["Помидоры"].id, amount=0.06),
        Compound(dish_id=d["Овощной салат"].id, product_id=pr["Огурцы"].id, amount=0.06),
        Compound(dish_id=d["Овощной салат"].id, product_id=pr["Масло растительное"].id, amount=0.01),

        Compound(dish_id=d["Фрукты (яблоко/банан)"].id, product_id=pr["Яблоки"].id, amount=0.10),
        Compound(dish_id=d["Фрукты (яблоко/банан)"].id, product_id=pr["Бананы"].id, amount=0.10),
    ]
    db.session.add_all(compounds)

    # --- меню на дни ---
    menus = []
    for day in daterange(start, days):
        menus.append(Menu(date=day, type=MealType.BREAKFAST))
        menus.append(Menu(date=day, type=MealType.LUNCH))
    db.session.add_all(menus)
    db.session.flush()

    # Привязка блюд к меню (MenuDishes)
    # Завтраки чередуем
    breakfast_sets = [
        ["Овсяная каша на молоке", "Чай с сахаром", "Фрукты (яблоко/банан)"],
        ["Омлет", "Чай с сахаром", "Бутерброд с сыром"],
    ]
    # Обеды чередуем (в т.ч. рыба раз в 3 дня)
    lunch_sets = [
        ["Куриный суп", "Гречка с курицей", "Овощной салат"],
        ["Куриный суп", "Рис с говядиной", "Овощной салат"],
        ["Куриный суп", "Рыба с картофелем", "Овощной салат"],
    ]

    md_rows = []
    for i in range(days):
        day = start + timedelta(days=i)
        # найти меню на день
        b_menu = next(m for m in menus if m.date == day and m.type == MealType.BREAKFAST)
        l_menu = next(m for m in menus if m.date == day and m.type == MealType.LUNCH)

        bset = breakfast_sets[i % len(breakfast_sets)]
        lset = lunch_sets[i % len(lunch_sets)]

        for dish_name in bset:
            md_rows.append(MenuDishes(menu_id=b_menu.id, dish_id=d[dish_name].id))
        for dish_name in lset:
            md_rows.append(MenuDishes(menu_id=l_menu.id, dish_id=d[dish_name].id))

    db.session.add_all(md_rows)

    # --- оплаты (PaidMenu) ---
    # студент1 покупает все завтраки, студент2 покупает все обеды, студент3 покупает первые 3 дня
    paid_rows = []
    for i in range(days):
        day = start + timedelta(days=i)
        b_menu = next(m for m in menus if m.date == day and m.type == MealType.BREAKFAST)
        l_menu = next(m for m in menus if m.date == day and m.type == MealType.LUNCH)

        paid_rows.append(PaidMenu(user_id=u["student1@example.com"].id, menu_id=b_menu.id, is_taken=(i % 2 == 0)))
        paid_rows.append(PaidMenu(user_id=u["student2@example.com"].id, menu_id=l_menu.id, is_taken=(i % 3 != 0)))

        if i < 3:
            paid_rows.append(PaidMenu(user_id=u["student3@example.com"].id, menu_id=b_menu.id, is_taken=False))
            paid_rows.append(PaidMenu(user_id=u["student3@example.com"].id, menu_id=l_menu.id, is_taken=False))

    db.session.add_all(paid_rows)

    # --- отзывы (Feedback) ---
    # Пара отзывов на разные дни/блюда
    some_menus = sorted(menus, key=lambda x: (x.date, x.type.value))
    feedbacks = [
        Feedback(
            text="Каша вкусная, но хотелось бы меньше сахара.",
            user_id=u["student1@example.com"].id,
            menu_id=some_menus[0].id,
            dish_id=d["Овсяная каша на молоке"].id
        ),
        Feedback(
            text="Суп отличный, порции достаточно.",
            user_id=u["student2@example.com"].id,
            menu_id=some_menus[3].id,
            dish_id=d["Куриный суп"].id
        ),
        Feedback(
            text="Салат свежий, но мало масла.",
            user_id=u["student3@example.com"].id,
            menu_id=some_menus[5].id,
            dish_id=d["Овощной салат"].id
        ),
    ]
    db.session.add_all(feedbacks)

    # --- заявки на продукты (ProductRequest) ---
    requests = [
        ProductRequest(product_id=pr["Рыба (филе)"].id, amount=5.0, is_agreed=False, created=start + timedelta(days=1)),
        ProductRequest(product_id=pr["Яблоки"].id, amount=10.0, is_agreed=True, created=start + timedelta(days=2), fulfilled=start + timedelta(days=4)),
        ProductRequest(product_id=pr["Хлеб"].id, amount=30.0, is_agreed=True, created=start + timedelta(days=0), fulfilled=start + timedelta(days=1)),
    ]
    db.session.add_all(requests)

    db.session.commit()
    return {"start": start.isoformat(), "days": days}
    