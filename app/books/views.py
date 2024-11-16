from django.contrib import messages
from django.http import JsonResponse
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

# View to add books manually
@user_passes_test(check_user_authenticated, login_url='/users/login', redirect_field_name='next')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            OwnedBook.objects.create(user=request.user, isbn=book)
            
            # Return a JSON response for AJAX call
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'There was an error with your form.'})
    else:
        form = BookForm()
    
    # Return the form for the GET request
    return {'form': form}

# Overview all owned books
@user_passes_test(check_user_authenticated, login_url='/users/login', redirect_field_name='next')
def owned_books(request):
    user_books = OwnedBook.objects.filter(user=request.user)
    form_context = add_book(request)
    if isinstance(form_context, JsonResponse):
        return form_context
    form = form_context.get('form')
    return render(request, 'books/mybooks.html', {'books': user_books, 'form': form})


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


