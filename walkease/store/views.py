from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required  # ✅ Ensures login protection
from walkease.store.models import Product, Category, Order


def index(request):
    """ Homepage view """
    return render(request, "store/index.html")


def product_list(request):
    """ Displays products, filtered by category if selected """
    category_name = request.GET.get("category")

    if category_name:
        category = Category.objects.filter(name__iexact=category_name).first()
        products = Product.objects.filter(category=category) if category else Product.objects.none()
    else:
        products = Product.objects.all()

    return render(request, "store/productlist.html", {"products": products, "category": category_name})


@login_required
def buy_product(request, product_id):
    """ Handles purchasing a product with login required """
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))

        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            total_price=product.price * quantity,
        )
        return redirect("store:order_success", order_id=order.id)

    return render(request, "store/buy_product.html", {"product": product})
