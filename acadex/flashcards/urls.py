from django.urls import path
from . import views

urlpatterns = [
    path('', views.flashcard_list, name='flashcard_list'),
    path('create/', views.create_flashcard, name='create_flashcard'),
    path('<int:flashcard_id>/study/', views.study_flashcard, name='study_flashcard'),
]