from django.urls import path
from . import views
urlpatterns = [
    path('practice/', views.practice_list, name='practice_list'),
    path('practice/<slug:subject_slug>/<slug:topic_slug>/', views.practice_by_topic, name='practice_by_topic'),
]
