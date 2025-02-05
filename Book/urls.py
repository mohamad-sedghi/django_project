from django.urls import path
from .views import toggle_like
from . import views


app_name = 'Book'
urlpatterns = [
    path('', views.index, name='index'),
    path('sign-up/', views.register, name='sign_up'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('book-detail/<int:pk>/',views.book_detail,name='book_detail'), 
    path('delete-comment/<int:pk>/', views.delete_comment, name='delete_comment'),
    path('book/like/<int:pk>/', views.toggle_like, name='toggle_like'),
    path('add/', views.add_book, name='add_book'),
    path('edit/<int:pk>/', views.edit_book, name='edit_book'),
    path('delete/<int:pk>/', views.delete_book, name='delete_book'),
]
