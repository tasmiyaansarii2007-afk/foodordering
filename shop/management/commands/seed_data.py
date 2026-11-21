from django.core.management.base import BaseCommand
from django.utils.text import slugify
from shop.models import Category, Product

class Command(BaseCommand):
    help = "Create sample food categories and products."

    def handle(self, *args, **options):
        samples = {
            "Burgers": [
                ("Classic Veg Burger", "Crispy veg patty, lettuce and house sauce.", "129.00",
                 "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=900"),
                ("Paneer Tikka Burger", "Grilled paneer with mint mayo.", "169.00",
                 "https://images.unsplash.com/photo-155 burger?w=900"),
            ],
            "Pizza": [
                ("Margherita Pizza", "Classic cheese and tomato pizza.", "219.00",
                 "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=900"),
                ("Farmhouse Pizza", "Onion, capsicum, mushroom and cheese.", "299.00",
                 "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=900"),
            ],
            "Sides": [
                ("French Fries", "Golden, crispy salted fries.", "89.00",
                 "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=900"),
                ("Garlic Bread", "Toasted bread with garlic butter.", "99.00",
                 "https://images.unsplash.com/photo-1573140247632-f8fd74997d5c?w=900"),
            ],
            "Drinks": [
                ("Cold Coffee", "Chilled creamy coffee.", "119.00",
                 "https://images.unsplash.com/photo-146 pancoffee?w=900"),
                ("Fresh Lime Soda", "Refreshing sweet and salty lime soda.", "69.00",
                 "https://images.unsplash.com/photo-1513558161293-cाद?w=900"),
            ],
        }
        # Replace any intentionally generic/invalid sample image links with known working fallback URLs.
        fallback_images = [
            "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=900",
            "https://images.unsplash.com/photo-1550547660-d9450f859349?w=900",
            "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=900",
            "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=900",
            "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=900",
            "https://images.unsplash.com/photo-1573140247632-f8fd74997d5c?w=900",
            "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=900",
            "https://images.unsplash.com/photo-1513558161293-cd6c6a1a5a8d?w=900",
        ]
        image_index = 0
        for category_name, products in samples.items():
            category, _ = Category.objects.get_or_create(
                slug=slugify(category_name), defaults={"name": category_name}
            )
            for name, description, price, image_url in products:
                image_url = fallback_images[image_index]
                image_index += 1
                Product.objects.get_or_create(
                    category=category, name=name,
                    defaults={"description": description, "price": price, "image_url": image_url}
                )
        self.stdout.write(self.style.SUCCESS("Sample categories and food products are ready."))
