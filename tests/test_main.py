import unittest
from main import Product, Category


class TestProduct(unittest.TestCase):
    def setUp(self):
        self.product = Product("Телефон", "Смартфон", 1000.0, 10)

    def test_init(self):
        self.assertEqual(self.product.name, "Телефон")
        self.assertEqual(self.product.description, "Смартфон")
        self.assertEqual(self.product.price, 1000.0)
        self.assertEqual(self.product.quantity, 10)

    def test_price_setter(self):
        self.product.price = 2000.0
        self.assertEqual(self.product.price, 2000.0)

    def test_price_setter_negative(self):
        with self.assertRaises(ValueError):
            self.product.price = -1000.0

    def test_str(self):
        expected = "Телефон, 1000.0 руб. Остаток: 10 шт."
        self.assertEqual(str(self.product), expected)

    def test_add(self):
        product2 = Product("Ноутбук", "Портативный компьютер", 2000.0, 5)
        total_price = self.product + product2
        self.assertEqual(total_price, 20000.0)

    def test_add_different_types(self):
        with self.assertRaises(TypeError):
            result = self.product + "строка"


class TestCategory(unittest.TestCase):
    def setUp(self):
        self.category = Category("Электроника", "Технические устройства")
        self.product1 = Product("Телефон", "Смартфон", 1000.0, 10)
        self.product2 = Product("Ноутбук", "Портативный компьютер", 2000.0, 5)

    def test_init(self):
        self.assertEqual(self.category.name, "Электроника")
        self.assertEqual(self.category.description, "Технические устройства")
        self.assertEqual(self.category.products, "")

    def test_add_product(self):
        self.category.add_product(self.product1)
        self.assertEqual(self.category.products, "Телефон, 1000.0 руб. Остаток: 10 шт.")

    def test_add_multiple_products(self):
        self.category.add_product(self.product1)
        self.category.add_product(self.product2)
        expected = "Телефон, 1000.0 руб. Остаток: 10 шт.\nНоутбук, 2000.0 руб. Остаток: 5 шт."
        self.assertEqual(self.category.products, expected)

    def test_add_invalid_product(self):
        with self.assertRaises(TypeError):
            self.category.add_product("не продукт")

    def test_str(self):
        self.category.add_product(self.product1)
        expected = "Электроника, количество продуктов: 10 шт."
        self.assertEqual(str(self.category), expected)

    def test_len(self):
        self.category.add_product(self.product1)
        self.category.add_product(self.product2)
        self.assertEqual(len(self.category), 15)

    def test_average_price(self):
        self.category.add_product(self.product1)
        self.category.add_product(self.product2)
        self.assertEqual(self.category.average_price(), 1500.0)

    def test_average_price_no_products(self):
        self.assertEqual(self.category.average_price(), 0)

    def test_products_property(self):
        self.category.add_product(self.product1)
        expected = "Телефон, 1000.0 руб. Остаток: 10 шт."
        self.assertEqual(self.category.products, expected)


if __name__ == '__main__':
    unittest.main() 