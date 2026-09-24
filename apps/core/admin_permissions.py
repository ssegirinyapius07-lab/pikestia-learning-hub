from django.contrib import admin


class AdminOnlyModelAdmin(admin.ModelAdmin):
    """Allow only administrators/superusers to access this admin model."""

    def _is_admin(self, request):
        return bool(request.user.is_superuser or request.user.role == 'admin')

    def has_module_permission(self, request):
        return self._is_admin(request)

    def has_view_permission(self, request, obj=None):
        return self._is_admin(request)

    def has_add_permission(self, request):
        return self._is_admin(request)

    def has_change_permission(self, request, obj=None):
        return self._is_admin(request)

    def has_delete_permission(self, request, obj=None):
        return self._is_admin(request)
