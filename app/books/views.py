from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Book, Shelf, OwnedBook
from .forms import BookForm, ShelfForm
import requests


# User Authenticated     
def check_user_authenticated(user):
    return user.is_authenticated

def save_and_create_owned_book(form, model, user, commit=False):
    """
    Generic function to handle form validation, saving an object, 
    and creating an OwnedBook if it's a book.
    :param form: The form to validate and save
    :param model: The model class (either Shelf or Book)
    :param user: The user object to associate with the model
    :param commit: Whether to commit the save immediately or not
    :return: JsonResponse indicating success or failure
    """
    if form.is_valid():
        obj = form.save(commit=commit)
        if not commit:
            obj.user = user
            obj.save()

        # If it's a book, create the OwnedBook
        if model == Book:
            OwnedBook.objects.create(user=user, isbn=obj)

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': f'{model.__name__} could not be added.'})

@user_passes_test(check_user_authenticated, login_url='/users/login', redirect_field_name='next')
def add_item(request, item_type):
    """
    Generic view to add either a shelf or a book based on the item_type parameter.
    :param item_type: Can be 'shelf' or 'book'
    """
    form = None
    model = None
    
    if item_type == 'shelf':
        form = ShelfForm(request.POST or None)
        model = Shelf
    elif item_type == 'book':
        form = BookForm(request.POST, request.FILES or None)
        model = Book
    else:
        return JsonResponse({'success': False, 'error': 'Invalid item type.'})

    if request.method == 'POST':
        return save_and_create_owned_book(form, model, request.user, commit=False)

    return {'form': form}

@user_passes_test(check_user_authenticated, login_url='/users/login', redirect_field_name='next')
def add_item(request, item_type):
    """
    Generic view to add either a shelf or a book based on the item_type parameter.
    :param item_type: Can be 'shelf' or 'book'
    """
    form = None
    model = None
    
    if item_type == 'shelf':
        form = ShelfForm(request.POST or None)
        model = Shelf
    elif item_type == 'book':
        form = BookForm(request.POST, request.FILES or None)
        model = Book
    else:
        return JsonResponse({'success': False, 'error': 'Invalid item type.'})

    if request.method == 'POST':
        return save_and_create_owned_book(form, model, request.user, commit=False)

    return {'form': form}

# Overview Shelves
@user_passes_test(check_user_authenticated, login_url='/users/login', redirect_field_name='next')
def shelves(request):
    user_shelves = Shelf.objects.filter(user=request.user)
    form_context = add_item(request, 'shelf')  
    if isinstance(form_context, JsonResponse):
        return form_context
    form = form_context.get('form')
    return render(request, 'books/shelves.html', {'shelves': user_shelves, 'form': form})

# Overview all owned books
@user_passes_test(check_user_authenticated, login_url='/users/login', redirect_field_name='next')
def owned_books(request):
    user_books = OwnedBook.objects.filter(user=request.user)
    form_context = add_item(request, 'book')  
    if isinstance(form_context, JsonResponse):
        return form_context
    form = form_context.get('form')
    return render(request, 'books/mybooks.html', {'books': user_books, 'form': form})

# Search for books
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


