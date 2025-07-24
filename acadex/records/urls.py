from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_record, name='upload_record'),
    path('', views.view_records, name='view_records'),
]