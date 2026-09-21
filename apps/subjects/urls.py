from django.urls import path
from . import views
urlpatterns = [
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/<slug:slug>/', views.subject_detail, name='subject_detail'),
    path('subjects/<slug:subject_slug>/<slug:topic_slug>/', views.topic_detail, name='topic_detail'),
]
