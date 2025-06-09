from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("profile/", views.profile_detail, name="profile_detail"),
    path("profile/update/", views.update_profile, name="update_profile"),
]