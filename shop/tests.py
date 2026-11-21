from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Product

class ShopSmokeTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Snacks", slug="snacks")
        Product.objects.create(category=category, name="Test Burger", price="99.00", is_available=True)

    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Burger")

    def test_products_api(self):
        response = self.client.get(reverse("api_products"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)

    def test_checkout_requires_login(self):
        response = self.client.get(reverse("checkout"))
        self.assertEqual(response.status_code, 302)
