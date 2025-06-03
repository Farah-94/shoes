from django.urls import path
from . import views  # Assumes you have a views.py in the store app

urlpatterns = [
    # The empty string '' means this view will handle the base URL for this app
    path('', views.index, name='store-index'),
]