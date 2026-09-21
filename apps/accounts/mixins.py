from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        u = self.request.user
        return u.is_authenticated and (u.role == 'admin' or u.is_superuser)
    def handle_no_permission(self):
        raise PermissionDenied
