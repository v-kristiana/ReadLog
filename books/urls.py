from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('add/', views.book_create, name='book_add'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    path('<int:book_id>/edit/', views.book_edit, name='book_edit'),
    path('<int:book_id>/delete/', views.book_delete, name='book_delete'),
    path('search/', views.search_books, name='search_books'),
    path('my-books/', views.my_books, name='my_books'),
    path('<int:book_id>/favourite/', views.toggle_favourite, name='toggle_favourite'),
    path('<int:book_id>/status/', views.set_reading_status, name='set_reading_status'),
]