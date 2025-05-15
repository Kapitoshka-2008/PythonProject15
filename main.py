class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price  # Приватный атрибут цены
        self.quantity = quantity

    @classmethod
    def new_product(cls, product_data: dict):
        """
        Создает и возвращает экземпляр класса Product на основе данных словаря.
        """
        # Проверка наличия всех ключей для большей надежности (опционально)
        # required_keys = {'name', 'description', 'price', 'quantity'}
        # if not required_keys.issubset(product_data.keys()):
        #     raise ValueError(f"Словарь должен содержать ключи: {required_keys}")
        return cls(product_data['name'], product_data['description'], product_data['price'], product_data['quantity'])

    @property
    def price(self):
        """Геттер для приватного атрибута цены."""
        return self.__price

    @price.setter
    def price(self, new_price: float):
        """Сеттер для приватного атрибута цены."""
        if isinstance(new_price, (int, float)) and new_price > 0:
            self.__price = float(new_price)
        else:
            print("Цена не должна быть нулевая или отрицательная")

    def __str__(self):
        """Строковое представление продукта."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."


class Category:
    category_count = 0  # Счетчик общего числа категорий
    product_count = 0   # Класс-атрибут «счетчик продуктов»

    def __init__(self, name: str, description: str, products_list: list = None):
        self.name = name
        self.description = description
        # Атрибут списка товаров класса Category имеет приватный режим доступа.
        self.__products = products_list if products_list is not None else []
        Category.category_count += 1
        # Изначальные продукты в списке не увеличивают Category.product_count,
        # так как это происходит только через метод add_product.

    def add_product(self, product):
        """
        Добавляет продукт в приватный атрибут __products.
        Прибавляет 1 к класс-атрибуту «счетчик продуктов».
        """
        if not isinstance(product, Product):
            print("Ошибка: можно добавлять только объекты класса Product.")
            return

        self.__products.append(product)
        Category.product_count += 1  # Увеличиваем класс-атрибут

    @property
    def products(self):
        """
        Геттер для приватного атрибута __products.
        Возвращает строку со всеми продуктами в формате:
        "Название продукта, X руб. Остаток: X шт.\n"
        """
        if not self.__products:
            return "Список товаров пуст.\n"
        
        product_output_string = ""
        for prod in self.__products:
            product_output_string += f"{prod.name}, {prod.price} руб. Остаток: {prod.quantity} шт.\n"
        return product_output_string


if __name__ == "__main__":
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    print(f"Товары в категории {category1.name} до добавления:")
    print(category1.products) # Выведет список из 3 товаров

    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category1.add_product(product4) # Category.product_count станет 1

    print(f"Товары в категории {category1.name} после добавления:")
    print(category1.products) # Выведет список из 4 товаров
    
    # Этот print выведет значение класс-атрибута Category.product_count
    print(f"Общий счетчик добавленных продуктов (Category.product_count): {category1.product_count}")

    # Тестирование Product.new_product()
    print("\nТестирование Product.new_product():")
    new_product_data = {
        "name": "Test Product via new_product",
        "description": "Created using classmethod",
        "price": 999.99,
        "quantity": 20
    }
    created_product = Product.new_product(new_product_data)
    print(f"Создан товар: {created_product.name}, Цена: {created_product.price}, Количество: {created_product.quantity}")

    # Тестирование сеттера цены
    print("\nТестирование сеттера цены для товара:", created_product.name)
    print(f"Начальная цена: {created_product.price}")
    
    created_product.price = 1200.0
    print(f"Цена после установки 1200.0: {created_product.price}")

    print("Попытка установить цену -100:")
    created_product.price = -100  # Должно вывести сообщение об ошибке
    print(f"Цена после попытки установить -100: {created_product.price}") # Цена не должна измениться

    print("Попытка установить цену 0:")
    created_product.price = 0  # Должно вывести сообщение об ошибке
    print(f"Цена после попытки установить 0: {created_product.price}") # Цена не должна измениться

    print(f"\nВсего категорий создано: {Category.category_count}")

    # Пример изначального main.py пользователя (адаптированный)
    print("\n--- Изначальный блок main.py пользователя ---")
    user_product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    user_product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    user_product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    user_category1 = Category(
        "Смартфоны (User)",
        "Смартфоны от пользователя",
        [user_product1, user_product2, user_product3]
    )
    # Category.product_count был 1, после этого add_product станет 2
    
    print(user_category1.products)
    user_product4 = Product("55\" QLED 4K (User)", "Фоновая подсветка", 123000.0, 7)
    user_category1.add_product(user_product4) # Category.product_count станет 2
    print(user_category1.products)
    print(f"Category.product_count (после действий пользователя): {user_category1.product_count}") # Ожидается 2

    new_product_instance_user = Product.new_product(
        {"name": "Samsung Galaxy S23 Ultra (User)", "description": "256GB, Серый цвет, 200MP камера (User)", "price": 180000.0,
         "quantity": 5})
    print(new_product_instance_user.name)
    print(new_product_instance_user.description)
    print(new_product_instance_user.price)
    print(new_product_instance_user.quantity)

    new_product_instance_user.price = 800
    print(f"Цена {new_product_instance_user.name} после установки 800: {new_product_instance_user.price}")

    new_product_instance_user.price = -100
    print(f"Цена {new_product_instance_user.name} после попытки установить -100: {new_product_instance_user.price}")
    new_product_instance_user.price = 0
    print(f"Цена {new_product_instance_user.name} после попытки установить 0: {new_product_instance_user.price}") 