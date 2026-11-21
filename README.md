# QuickBite – Django Online Food Ordering System

A ready-to-run Django project for a college/demo project. It uses SQLite and Django's built-in authentication.

## Features
- Customer registration, login and logout
- Food categories and product listing
- Search and category filtering
- Session-based shopping cart (add, update quantity, remove)
- Checkout with customer address and phone
- Order confirmation and customer order history
- Admin panel for managing categories, products and orders
- Simple JSON API endpoints for products and orders
- Responsive Bootstrap-based interface

> Payments are intentionally **Cash on Delivery/demo only**. No real payment gateway or delivery integration is configured.

## Requirements
- Python 3.10+
- pip

## Run on Windows (PowerShell or CMD)

1. Extract this ZIP.
2. Open a terminal in the extracted `food_ordering_system` folder.
3. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Create database tables:

```bash
python manage.py makemigrations shop
python manage.py migrate
```

6. Add demo food items:

```bash
python manage.py seed_data
```

7. Create an admin account:

```bash
python manage.py createsuperuser
```

8. Start the server:

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.
Admin: http://127.0.0.1:8000/admin/

## Run on macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations shop
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser
python manage.py runserver
```

## Demo flow
1. Register a customer account.
2. Browse the menu and add food to cart.
3. Open Cart, update quantities if needed, and proceed to checkout.
4. Submit an address and phone number.
5. View the order confirmation and order history.

## Admin usage
Log in at `/admin/` using the superuser you created. Add/edit categories and food products, upload product image URLs, and update order status.

## API endpoints
- `GET /api/products/` – list active products as JSON
- `GET /api/orders/` – list the logged-in user's orders (login required)

## Project structure

```text
food_ordering_system/
├── manage.py
├── requirements.txt
├── README.md
├── foodorder/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── shop/
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    ├── forms.py
    ├── cart.py
    ├── migrations/
    ├── management/commands/seed_data.py
    └── templates/shop/
```

## Notes
- SQLite database is created after running migrations.
- Product images use external image URLs; internet is required to display them. If an image URL is empty, a fallback placeholder is shown.
- `SECRET_KEY` and `DEBUG` are suitable only for local development. Change them before deployment.
