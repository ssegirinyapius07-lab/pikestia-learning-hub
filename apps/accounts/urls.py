from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register_view, name='account_register'),
    path('profile/', views.profile_view, name='account_profile'),
    path('settings/', views.settings_view, name='account_settings'),
    path('settings/theme/', views.update_theme_ajax, name='account_theme_update'),
    path('settings/password/', views.change_password_view, name='account_password_change'),
]
