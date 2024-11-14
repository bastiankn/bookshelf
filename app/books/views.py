from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Book, Shelf, OwnedBook
from .forms import BookForm
import requests


# User Authenticated     
def check_user_authenticated(user):
    return user.is_authenticated

# Overview Shelves
@user_passes_test(check_user_authenticated, login_url='/users/login', redirect_field_name='next')
def shelves(request):
    user_shelves = Shelf.objects.filter(user=request.user)
    return render(request, 'books/shelves.html', {'shelves': user_shelves})

# Overview all owned books
@user_passes_test(check_user_authenticated, login_url='/users/login', redirect_field_name='next')
def owned_books(request):
    user_books = OwnedBook.objects.filter(user=request.user)
    return render(request, 'books/mybooks.html', {'books': user_books})

# add books manually
@user_passes_test(check_user_authenticated, login_url='/users/login', redirect_field_name='next')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)  # Handle file uploads for cover_image
        if form.is_valid():
            book = form.save(commit=False)
            book.save()

            owned_book = OwnedBook(user=request.user, isbn=book)  
            owned_book.save()

            messages.success(request, 'Book added successfully and associated with your account.')
            return redirect('owned_books')  
        else:
            messages.error(request, 'There was an error with your form.')
    else:
        form = BookForm()

    return render(request, 'books/add_book.html', {'form': form})

# search for books
@user_passes_test(check_user_authenticated, login_url='/users/login', redirect_field_name='next')
def search_books(request):
    query = request.GET.get('q')
    results = []
    if query:
        # Use Google Books API to search for books
        response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={query}')
        if response.status_code == 200:
            data = response.json()
            results = data.get('items', [])
    return render(request, 'books/search_book.html', {'results': results})


