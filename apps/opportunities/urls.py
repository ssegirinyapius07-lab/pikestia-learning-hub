from django.urls import path
from . import views
urlpatterns = [
    path('opportunities/', views.opp_list, name='opp_list'),
    path('opportunities/<slug:slug>/', views.opp_detail, name='opp_detail'),
]
