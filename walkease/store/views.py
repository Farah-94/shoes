from django.shortcuts       import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http            import HttpResponse
from django.conf            import settings

from .models import Product, Order, OrderItem, Review
from .forms  import ReviewForm

def index(request):
    """Homepage."""
    return render(request, "store/index.html")


def product_list(request):
    """
    Display all products.
    If you want to filter by category later, you can accept a `category` GET param.
    """
    products = Product.objects.all()
    return render(
        request,
        "store/productlist.html",
        {"products": products}
    )


def product_detail(request, product_id):
    """Show a single product’s detail page."""
    product = get_object_or_404(Product, id=product_id)
    return render(
        request,
        "store/product_detail.html",
        {"product": product}
    )


@login_required
def buy_product(request, product_id):
    """
    Handles:
      1) Adding to cart (POST with name="add_to_cart")
      2) Posting a review (POST with name="submit_review")
    """
    product = get_object_or_404(Product, id=product_id)

    # --- 1) Add to cart logic ---
    if request.method == "POST" and request.POST.get("add_to_cart"):
        quantity = request.POST.get("quantity", 1)
        try:
            quantity = int(quantity)
            if quantity < 1:
                raise ValidationError("Quantity must be at least 1.")
            if quantity > product.stock:
                raise ValidationError("Not enough stock available.")
        except (ValueError, ValidationError) as e:
            return HttpResponse(str(e), status=400)

        # Create an OrderItem, then attach it to a (new or existing) Order
        item = OrderItem.objects.create(
            product=product,
            quantity=quantity,
            size=request.POST.get("size", "")
        )
        order, created = Order.objects.get_or_create(
            user=request.user,
            status="Cart"
        )
        order.items.add(item)
        order.total_price += product.price * quantity
        order.save()
        return redirect("cart:view_cart")

    # --- 2) Review logic ---
    review_form = ReviewForm()
    if request.method == "POST" and request.POST.get("submit_review"):
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user    = request.user
            review.save()
            return redirect("store:buy_product", product_id=product.id)

    # GET or invalid POST – render the page with context
    return render(request, "store/buy_product.html", {
        "product":     product,
        "reviews":     product.reviews.all(),  # using related_name="reviews"
        "review_form": review_form,
    })


def contact(request):
    """
    A simple contact page – on POST you could:
      • Send an email via Django’s EmailMessage,
      • Save it to a database table,
      • Or forward to Formspree.
    """
    if request.method == "POST":
        # Example: just echo back
        name    = request.POST.get("name")
        email   = request.POST.get("email")
        message = request.POST.get("message")
        # TODO: send email or save to DB
        return redirect("store:index")

    return render(request, "store/contact.html")