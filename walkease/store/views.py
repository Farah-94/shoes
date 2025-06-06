from django.shortcuts import redirect, render, get_object_or_404
from store.models import Product, Category
from django.http import HttpResponse







def index(request):
     return render(request, 'store/index.html')






def product_list(request):
    category_name = request.GET.get("category", None)  # ✅ Get category from URL

    if category_name:
        category = Category.objects.filter(name__iexact=category_name).first()
        products = Product.objects.filter(category=category) if category else Product.objects.none()
    else:
        products = Product.objects.all()  # ✅ Show all products if no category filter

    return render(request, "store/productlist.html", {"products": products})

def buy_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=request.POST.get("quantity", 1),
            total_price=product.price * int(request.POST.get("quantity", 1)),
        )
        return redirect("store:order_success", order_id=order.id)
    return render(request, "store/buy_product.html", {"product": product})