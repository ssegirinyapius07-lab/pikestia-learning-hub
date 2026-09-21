from django.urls import path
from . import views
urlpatterns = [
    path('learn/', views.resource_list, name='resource_list'),
    path('learn/<slug:subject_slug>/<slug:topic_slug>/<slug:resource_slug>/', views.resource_detail, name='resource_detail'),
]
