from django.urls import path
from . import views


app_name = 'Book'
urlpatterns = [
    path('', views.index, name='index'),
    path('sign-up/', views.register, name='sign_up'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
