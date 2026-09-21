from django.urls import path
from . import views
urlpatterns = [
    path('bookmarks/', views.my_bookmarks, name='my_bookmarks'),
    path('bookmarks/toggle/', views.toggle_bookmark, name='toggle_bookmark'),
]
