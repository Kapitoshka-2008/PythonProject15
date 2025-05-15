import unittest
from main import Product, Category, Smartphone, LawnGrass


class TestProduct(unittest.TestCase):
    def setUp(self):
        self.product = Product("Test Product", "Test Description", 100.0, 10)

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.description, "Test Description")
        self.assertEqual(self.product.price, 100.0)
        self.assertEqual(self.product.quantity, 10)

    def test_price_setter(self):
        self.product.price = 150.0
        self.assertEqual(self.product.price, 150.0)
        self.product.price = -50.0
        self.assertEqual(self.product.price, 150.0)

    def test_str_method(self):
        expected_str = "Test Product, 100.0 руб. Остаток: 10 шт."
        self.assertEqual(str(self.product), expected_str)

    def test_add_method(self):
        product2 = Product("Test Product 2", "Test Description 2", 200.0, 5)
        total_value = self.product + product2
        self.assertEqual(total_value, 2000.0)  # (100 * 10) + (200 * 5)


class TestCategory(unittest.TestCase):
    def setUp(self):
        self.category = Category("Test Category", "Test Description")
        self.product1 = Product("Product 1", "Description 1", 100.0, 10)
        self.product2 = Product("Product 2", "Description 2", 200.0, 5)

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Test Category")
        self.assertEqual(self.category.description, "Test Description")
        self.assertEqual(len(self.category.products), 0)

    def test_add_product(self):
        self.category.add_product(self.product1)
        self.assertEqual(len(self.category.products), 1)
        self.assertEqual(self.category.products[0], self.product1)

    def test_products_property(self):
        self.category.add_product(self.product1)
        self.category.add_product(self.product2)
        products_str = self.category.products_str()
        self.assertIn("Product 1, 100.0 руб. Остаток: 10 шт.", products_str)
        self.assertIn("Product 2, 200.0 руб. Остаток: 5 шт.", products_str)

    def test_average_price(self):
        self.assertEqual(self.category.average_price(), 0)
        self.category.add_product(self.product1)
        self.category.add_product(self.product2)
        self.assertEqual(self.category.average_price(), 150.0)


class TestSmartphone(unittest.TestCase):
    def setUp(self):
        self.smartphone = Smartphone("iPhone", "Latest model", 1000.0, 5, "High", "iPhone 13", "128GB", "Black")

    def test_smartphone_creation(self):
        self.assertEqual(self.smartphone.name, "iPhone")
        self.assertEqual(self.smartphone.description, "Latest model")
        self.assertEqual(self.smartphone.price, 1000.0)
        self.assertEqual(self.smartphone.quantity, 5)
        self.assertEqual(self.smartphone.performance, "High")
        self.assertEqual(self.smartphone.model, "iPhone 13")
        self.assertEqual(self.smartphone.memory, "128GB")
        self.assertEqual(self.smartphone.color, "Black")

    def test_str_method(self):
        expected_str = "iPhone, 1000.0 руб. Остаток: 5 шт."
        self.assertEqual(str(self.smartphone), expected_str)


class TestLawnGrass(unittest.TestCase):
    def setUp(self):
        self.lawn_grass = LawnGrass("Green Grass", "Fresh grass", 50.0, 100, "Russia", "2 weeks", "Green")

    def test_lawn_grass_creation(self):
        self.assertEqual(self.lawn_grass.name, "Green Grass")
        self.assertEqual(self.lawn_grass.description, "Fresh grass")
        self.assertEqual(self.lawn_grass.price, 50.0)
        self.assertEqual(self.lawn_grass.quantity, 100)
        self.assertEqual(self.lawn_grass.country, "Russia")
        self.assertEqual(self.lawn_grass.germination_period, "2 weeks")
        self.assertEqual(self.lawn_grass.color, "Green")

    def test_str_method(self):
        expected_str = "Green Grass, 50.0 руб. Остаток: 100 шт."
        self.assertEqual(str(self.lawn_grass), expected_str)


if __name__ == '__main__':
    unittest.main() 