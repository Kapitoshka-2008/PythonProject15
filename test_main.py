import pytest
from main import Product, Category # Assuming main.py is in the same directory or accessible in PYTHONPATH

# Fixture to reset Category class attributes before each test that needs it
@pytest.fixture(autouse=True)
def reset_category_counts():
    Category.category_count = 0
    Category.product_count = 0

# --- Тесты для класса Product ---

def test_product_creation():
    """Тест создания экземпляра Product и его атрибутов."""
    p = Product("Laptop", "High-performance laptop", 1500.00, 10)
    assert p.name == "Laptop"
    assert p.description == "High-performance laptop"
    assert p.quantity == 10
    # Доступ к приватной цене через геттер
    assert p.price == 1500.00

def test_product_price_is_private():
    """Тест, что атрибут __price действительно приватный."""
    p = Product("Test", "Test desc", 10.0, 1)
    with pytest.raises(AttributeError):
        print(p.__price) # Попытка прямого доступа

def test_product_price_getter():
    """Тест геттера цены."""
    p = Product("Mouse", "Wireless mouse", 25.00, 50)
    assert p.price == 25.00

def test_product_price_setter_valid():
    """Тест сеттера цены с корректным значением."""
    p = Product("Keyboard", "Mechanical keyboard", 75.00, 30)
    p.price = 80.00
    assert p.price == 80.00
    p.price = 0.01
    assert p.price == 0.01

def test_product_price_setter_invalid_zero(capsys):
    """Тест сеттера цены с нулевым значением."""
    p = Product("Screen", "4K Screen", 300.00, 5)
    initial_price = p.price
    p.price = 0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert p.price == initial_price # Цена не должна измениться

def test_product_price_setter_invalid_negative(capsys):
    """Тест сеттера цены с отрицательным значением."""
    p = Product("Webcam", "HD Webcam", 40.00, 15)
    initial_price = p.price
    p.price = -100
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert p.price == initial_price # Цена не должна измениться

def test_product_price_setter_invalid_type(capsys):
    """Тест сеттера цены с некорректным типом данных."""
    p = Product("Charger", "USB-C Charger", 20.00, 25)
    initial_price = p.price
    p.price = "invalid_price_type" # type: ignore 
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out # или другая ошибка в зависимости от реализации
    assert p.price == initial_price

def test_product_new_product_classmethod():
    """Тест класс-метода new_product."""
    product_data = {"name": "SSD", "description": "Fast SSD", "price": 120.00, "quantity": 20}
    p = Product.new_product(product_data)
    assert isinstance(p, Product)
    assert p.name == "SSD"
    assert p.description == "Fast SSD"
    assert p.price == 120.00
    assert p.quantity == 20

def test_product_str_representation():
    """Тест строкового представления продукта."""
    p = Product("Coffee Maker", "Drip coffee maker", 50.00, 5)
    assert str(p) == "Coffee Maker, 50 руб. Остаток: 5 шт."

# --- Тесты для класса Category ---

def test_category_creation_empty():
    """Тест создания категории без начальных продуктов."""
    c = Category("Electronics", "All kinds of electronics")
    assert c.name == "Electronics"
    assert c.description == "All kinds of electronics"
    # Доступ к приватному списку продуктов через геттер
    assert c.products == "Список товаров пуст.\n"
    assert Category.category_count == 1 # Счетчик категорий должен увеличиться

def test_category_creation_with_products():
    """Тест создания категории с начальным списком продуктов."""
    p1 = Product("Book", "A great book", 15.00, 10)
    p2 = Product("Pen", "A nice pen", 2.00, 100)
    c = Category("Stationery", "Pens and Books", [p1, p2])
    assert Category.category_count == 1
    expected_output = (
        "Book, 15 руб. Остаток: 10 шт.\n"
        "Pen, 2 руб. Остаток: 100 шт.\n"
    )
    assert c.products == expected_output
    # Category.product_count не должен изменяться при инициализации, только через add_product
    assert Category.product_count == 0


def test_category_products_is_private():
    """Тест, что атрибут __products действительно приватный."""
    c = Category("Test Category", "Test desc")
    with pytest.raises(AttributeError):
        print(c.__products) # Попытка прямого доступа


def test_category_add_product_single():
    """Тест добавления одного продукта в категорию."""
    c = Category("Groceries", "Food items")
    assert Category.product_count == 0 # Изначально 0
    p = Product("Milk", "Fresh milk", 3.00, 20)
    c.add_product(p)
    assert Category.product_count == 1 # Увеличился на 1
    expected_output = "Milk, 3 руб. Остаток: 20 шт.\n"
    assert c.products == expected_output

def test_category_add_product_multiple():
    """Тест добавления нескольких продуктов и проверки Category.product_count."""
    c1 = Category("Category1", "Desc1")
    p1 = Product("P1", "D1", 1.0, 1)
    p2 = Product("P2", "D2", 2.0, 2)
    
    initial_product_count = Category.product_count # Должен быть 0 из-за fixture
    
    c1.add_product(p1)
    assert Category.product_count == initial_product_count + 1
    
    c1.add_product(p2)
    assert Category.product_count == initial_product_count + 2
    
    c2 = Category("Category2", "Desc2") # Создание новой категории не влияет на product_count
    p3 = Product("P3", "D3", 3.0, 3)
    c2.add_product(p3)
    assert Category.product_count == initial_product_count + 3 # Общий счетчик
    
    expected_c1 = "P1, 1 руб. Остаток: 1 шт.\nP2, 2 руб. Остаток: 2 шт.\n"
    assert c1.products == expected_c1
    expected_c2 = "P3, 3 руб. Остаток: 3 шт.\n"
    assert c2.products == expected_c2

def test_category_add_invalid_product_type(capsys):
    """Тест добавления невалидного типа в add_product."""
    c = Category("Clothing", "Apparel")
    initial_product_count = Category.product_count
    c.add_product("Not a Product") # type: ignore
    captured = capsys.readouterr()
    assert "Ошибка: можно добавлять только объекты класса Product." in captured.out
    assert c.products == "Список товаров пуст.\n" # Список не должен измениться
    assert Category.product_count == initial_product_count # Счетчик не должен измениться

def test_category_products_getter_empty():
    """Тест геттера products для пустой категории."""
    c = Category("Empty Category", "Should be empty")
    assert c.products == "Список товаров пуст.\n"

def test_category_products_getter_formatting():
    """Тест форматирования вывода геттера products."""
    p1 = Product("Apple", "Red apple", 0.50, 50)
    p2 = Product("Banana", "Yellow banana", 0.30, 70)
    c = Category("Fruits", "Fresh fruits", [p1])
    c.add_product(p2) # p1 добавлен при инициализации, p2 через add_product
                      # Category.product_count станет 1 после add_product(p2)
    
    expected_output = (
        "Apple, 0.5 руб. Остаток: 50 шт.\n"
        "Banana, 0.3 руб. Остаток: 70 шт.\n"
    )
    assert c.products == expected_output
    assert Category.product_count == 1 # Только p2 был добавлен через add_product

def test_category_category_count_increment():
    """Тест инкремента счетчика категорий Category.category_count."""
    assert Category.category_count == 0 # Сброшено фикстурой
    Category("Cat1", "D1")
    assert Category.category_count == 1
    Category("Cat2", "D2")
    assert Category.category_count == 2
    Product("Prod independent", "Desc", 1,1) # Создание продукта не влияет
    assert Category.category_count == 2
    
def test_category_product_count_shared_and_incremented_by_add_product():
    """
    Тест, что Category.product_count является общим и инкрементируется 
    только методом add_product.
    """
    assert Category.product_count == 0 # Сброшено фикстурой

    p1 = Product("P1", "D1", 10, 1)
    p2 = Product("P2", "D2", 20, 2)
    p3 = Product("P3", "D3", 30, 3)

    cat1 = Category("C1", "DC1", [p1]) # p1 не влияет на product_count
    assert Category.product_count == 0 

    cat1.add_product(p2) # product_count становится 1
    assert Category.product_count == 1

    cat2 = Category("C2", "DC2")
    assert Category.product_count == 1 # Создание cat2 не влияет

    cat2.add_product(p3) # product_count становится 2
    assert Category.product_count == 2

    cat1.add_product(Product("P4", "D4", 40, 4)) # product_count становится 3
    assert Category.product_count == 3
    
    # Проверка содержимого категорий
    expected_cat1_products = (
        f"{p1.name}, {int(p1.price)} руб. Остаток: {p1.quantity} шт.\n"
        f"{p2.name}, {int(p2.price)} руб. Остаток: {p2.quantity} шт.\n"
        f"P4, 40 руб. Остаток: 4 шт.\n"
    )
    assert cat1.products == expected_cat1_products

    expected_cat2_products = (
        f"{p3.name}, {int(p3.price)} руб. Остаток: {p3.quantity} шт.\n"
    )
    assert cat2.products == expected_cat2_products 

def test_category_add_product_type_check():
    """Тест проверки типа добавляемого продукта."""
    c = Category("Test Category", "Test desc")
    
    # Тест с корректным типом
    p = Product("Test Product", "Test Description", 100.0, 1)
    c.add_product(p)
    assert Category.product_count == 1
    
    # Тест с некорректным типом
    c.add_product("Not a Product")  # type: ignore
    assert Category.product_count == 1  # Счетчик не должен измениться

def test_category_add_invalid_product_type(capsys):
    """Тест добавления невалидного типа в add_product."""
    c = Category("Clothing", "Apparel")
    initial_product_count = Category.product_count
    c.add_product("Not a Product")  # type: ignore
    captured = capsys.readouterr()
    assert "Ошибка: можно добавлять только объекты класса Product." in captured.out
    assert c.products == "Список товаров пуст.\n"
    assert Category.product_count == initial_product_count

def test_category_products_getter_empty():
    """Тест геттера products для пустой категории."""
    c = Category("Empty Category", "Should be empty")
    assert c.products == "Список товаров пуст.\n"

def test_category_products_getter_formatting():
    """Тест форматирования вывода геттера products."""
    p1 = Product("Apple", "Red apple", 0.50, 50)
    p2 = Product("Banana", "Yellow banana", 0.30, 70)
    c = Category("Fruits", "Fresh fruits", [p1])
    c.add_product(p2)
    
    expected_output = (
        "Apple, 0.5 руб. Остаток: 50 шт.\n"
        "Banana, 0.3 руб. Остаток: 70 шт.\n"
    )
    assert c.products == expected_output
    assert Category.product_count == 1 