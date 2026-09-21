from django.urls import path
from . import views
urlpatterns = [
    path('', views.home_view, name='home'),
    path('explore/', views.explore_view, name='explore'),
    path('search/', views.search_view, name='search'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('cookies/', views.cookie_policy_view, name='cookie_policy'),
    path('terms/', views.terms_view, name='terms'),
    path('acceptable-use/', views.acceptable_use_view, name='acceptable_use'),
    path('copyright/', views.copyright_view, name='copyright'),
    path('theme/set/', views.set_theme_view, name='set_theme'),
    path('cookies/set/', views.set_cookie_consent_view, name='set_cookie_consent'),
]
