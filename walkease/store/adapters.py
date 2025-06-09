from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import reverse

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        user = request.user

        if user.is_staff:  # ✅ Redirect staff/admin users
            return reverse("admin:index")
        else:  # ✅ Redirect regular customers
            return reverse("store:index")