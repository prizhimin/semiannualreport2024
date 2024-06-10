from django.contrib import admin
from django.urls import path, reverse_lazy, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views  # Добавлен импорт auth_views
from django.shortcuts import redirect


urlpatterns = [
    # path('', RedirectView.as_view(url=reverse_lazy('report_list')), name='home'),  # Исправлено 'report' на 'report_list'
    path('report/', include('sixmonths2024.urls')),
    path('admin/', admin.site.urls),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', lambda request: redirect('login', permanent=False)),  # Редирект на главную страницу приложения

]