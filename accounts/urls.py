from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('unregister/', views.unregister, name='unregister'),
    path('edit/', views.edit, name='edit'),
    path('password/', views.password, name='password'),
    path('<username>/', views.profile, name='profile'),
]
