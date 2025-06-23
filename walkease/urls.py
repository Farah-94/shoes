"""
URL configuration for walkease project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # your cart-based auth & cart views:
    path("cart/", include("walkease.cart.urls", namespace="cart")),

    # Allauth’s built-in URLs for e.g. account settings, password reset, social logins, etc.
    path("accounts/", include("allauth.urls")),

    # your other apps…
    path("user/",     include("walkease.user.urls",    namespace="user")),
    path("",          include("walkease.store.urls",   namespace="store")),
    path("checkout/", include("walkease.checkout.urls",namespace="checkout")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

