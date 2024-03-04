from django.contrib.admin import AdminSite
from django.contrib.auth.views import LogoutView

class CustomAdminSite(AdminSite):
    def get_logout(self, request):
        # Redirect to the regular login page
        return LogoutView.as_view(next_page='login')(request)

admin_site = CustomAdminSite()
