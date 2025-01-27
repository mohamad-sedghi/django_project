from django.urls import path
from . import views


app_name = 'Book'
urlpatterns = [
    path('', views.index, name='index'),
    path('sign-up/', views.register, name='sign_up'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('book-detail/<int:pk>/',views.book_detail,name='book_detail'), 
    path('delete-comment/<int:pk>/', views.delete_comment, name='delete_comment'),
]
