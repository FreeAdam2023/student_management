"""
@Time ： 2024-10-03
@Auth ： Adam Lyu
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('<int:pk>/', views.student_detail, name='student_detail'),
    path('add/', views.student_add, name='student_add'),
    path('edit/<int:pk>/', views.student_edit, name='student_edit'),
]
