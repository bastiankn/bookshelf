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

# Overview books in a specific shelf
@user_passes_test(check_user_authenticated, login_url='/users/login', redirect_field_name='next')
def shelved_books(request, shelf_name):
    shelf = get_object_or_404(Shelf, name=shelf_name, user=request.user)
    user_shelved_books = OwnedBook.objects.filter(user=request.user, shelf=shelf)
    return render(request, 'books/shelved_books.html', {
        'shelf': shelf,
        'books': user_shelved_books
    })

# add books manually
@user_passes_test(check_user_authenticated, login_url='/users/login', redirect_field_name='next')
def add_book(request):
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
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


