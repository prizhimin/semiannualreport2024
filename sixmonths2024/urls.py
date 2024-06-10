from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_report, name='create_report'),
    path('update/<int:pk>/', views.update_report, name='update_report'),
    path('', views.report_list, name='report_list'),
    # path('logout/', views.custom_logout_view, name='logout'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]