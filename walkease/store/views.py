from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.apps import apps
from .models import Product, Order  # ✅ Removed Category, using relative import




Product = apps.get_model("store", "Product")  # ✅ Dynamic Model Loading

def index(request):
    """ Homepage view """
    return render(request, "store/index.html")

from django.apps import apps

def get_product_detail(request, product_id):
    Product = apps.get_model("store", "Product")  # ✅ Dynamic model fetching
    product = get_object_or_404(Product, id=product_id)
    return render(request, "store/product_detail.html", {"product": product})




def product_list(request):
    """ Displays products, filtered by category if selected """

    products = Product.objects.filter(category=category) if category else Product.objects.all()

    return render(request, "store/productlist.html", {"products": products, "category": category_name})


def get_product_detail(request, product_id):
    """ Retrieves product details """
    product = get_object_or_404(Product, id=product_id)
    return render(request, "store/product_detail.html", {"product": product})


@login_required
def buy_product(request, product_id):
    """ Handles purchasing a product with login required """
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        quantity = request.POST.get("quantity", 1)

        try:
            quantity = int(quantity)
            if quantity < 1:
                raise ValidationError("Quantity must be at least 1.")
        except ValueError:
            return HttpResponse("Invalid quantity.", status=400)

        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            total_price=product.price * quantity,
        )
        return redirect("store:order_success", order_id=order.id)

    return render(request, "store/buy_product.html", {"product": product})


def contact(request):
    if request.method == "POST":
        # Process form submission here.
        # For example, retrieve form fields:
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        # You can then send an email, save to a database, or simply display a success message.
        return redirect("store:index")  # Redirect to a page after processing
    return render(request, "store/contact.html")  # Render a contact template if needed