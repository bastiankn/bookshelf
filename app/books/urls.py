from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # Route for all shelves a user created
    path('shelves/', views.shelves, name='shelves'),
    
    # Route for all books a user owns
    path('mybooks/', views.owned_books, name='owned_books'),
    
    # Route for searching books
    path('search/', views.search_books, name='search_book'),
]


# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)