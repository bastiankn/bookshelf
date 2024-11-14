from django.urls import path
from . import views

urlpatterns = [
    # Route for all shelves a user created
    path('shelves/', views.shelves, name='shelves'),
    
    # Route for all books a user owns
    path('mybooks/', views.owned_books, name='owned_books'),
    
    # Route for books in a specific shelf (using shelf name as a dynamic URL parameter)
    path('shelves/<str:shelf_name>/', views.shelved_books, name='shelved_books'),
    
    # Route to add a new book manually
    path('add/', views.add_book, name='add_book'),
    
    # Route for searching books
    path('search/', views.search_books, name='search_book'),
]