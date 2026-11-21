from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import CheckoutForm, RegisterForm
from .models import Category, Order, OrderItem, Product


def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True).select_related("category")
    category_slug = request.GET.get("category")
    search = request.GET.get("q", "").strip()
    if category_slug:
        products = products.filter(category__slug=category_slug)
    if search:
        products = products.filter(name__icontains=search) | products.filter(description__icontains=search)
    return render(request, "shop/home.html", {
        "categories": categories,
        "products": products.distinct(),
        "active_category": category_slug,
        "search_query": search,
    })


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Welcome to QuickBite! Your account is ready.")
        return redirect("home")
    return render(request, "shop/register.html", {"form": form})


def cart_detail(request):
    return render(request, "shop/cart.html", {"cart": Cart(request)})


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_available=True)
    try:
        quantity = max(1, min(int(request.POST.get("quantity", 1)), 20))
    except (TypeError, ValueError):
        quantity = 1
    Cart(request).add(product, quantity=quantity)
    messages.success(request, f"{product.name} added to your cart.")
    return redirect(request.POST.get("next") or "cart_detail")


@require_POST
def cart_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1
    cart = Cart(request)
    if quantity <= 0:
        cart.remove(product)
    else:
        cart.add(product, quantity=min(quantity, 20), override_quantity=True)
    return redirect("cart_detail")


@require_POST
def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Cart(request).remove(product)
    messages.info(request, f"{product.name} removed from your cart.")
    return redirect("cart_detail")


@login_required
def checkout(request):
    cart = Cart(request)
    items = list(cart)
    if not items:
        messages.info(request, "Your cart is empty.")
        return redirect("home")
    form = CheckoutForm(request.POST or None, initial={
        "full_name": f"{request.user.first_name}".strip() or request.user.username,
    })
    if request.method == "POST" and form.is_valid():
        order = form.save(commit=False)
        order.user = request.user
        order.total = sum((item["total_price"] for item in items), Decimal("0.00"))
        order.save()
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                product_name=item["product"].name,
                price=item["price"],
                quantity=item["quantity"],
            )
        cart.clear()
        messages.success(request, "Your order has been placed successfully.")
        return redirect("order_success", order_id=order.id)
    return render(request, "shop/checkout.html", {
        "form": form, "cart": cart, "items": items, "total": cart.get_total_price()
    })


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "shop/order_success.html", {"order": order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items")
    return render(request, "shop/my_orders.html", {"orders": orders})


def api_products(request):
    products = Product.objects.filter(is_available=True).select_related("category")
    data = [{
        "id": p.id, "name": p.name, "category": p.category.name,
        "description": p.description, "price": str(p.price), "image_url": p.image_url
    } for p in products]
    return JsonResponse({"count": len(data), "products": data})


@login_required
def api_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items")
    data = [{
        "id": o.id, "status": o.status, "total": str(o.total),
        "created_at": o.created_at.isoformat(),
        "items": [{"name": i.product_name, "quantity": i.quantity, "price": str(i.price)} for i in o.items.all()]
    } for o in orders]
    return JsonResponse({"count": len(data), "orders": data})
