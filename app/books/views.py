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
    and creating an OwnedBook if it's a book. Also handles the case
    where a book already exists and just associates it with the user.
    :param form: The form to validate and save
    :param model: The model class (either Shelf or Book)
    :param user: The user object to associate with the model
    :param commit: Whether to commit the save immediately or not
    :return: JsonResponse indicating success or failure
    """
    if model == Book:
            isbn=form.data.get('isbn')
            existing_book = Book.objects.filter(isbn=isbn).first()
            if existing_book:
                OwnedBook.objects.create(user=user, isbn=existing_book)
                return JsonResponse({'success': True})

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
        # Use API to search for books
        response = requests.get(f'https://openlibrary.org/search.json?q={query}')
        if response.status_code == 200:
            data = response.json()
            results = data.get('docs', [])

    if request.method == 'POST':
        # Process the POST request
        title = request.POST.get('title')
        author_name = request.POST.get('author_name')
        first_publish_year = request.POST.get('first_publish_year')
        isbn_string = request.POST.get('isbn')
        isbn_list = isbn_string.strip("[]").replace("'", "").split(", ")
        print(isbn_list)
        first_isbn = isbn_list[1]
        print(title)
        print(author_name)
        print(first_publish_year)
        print(first_isbn)
        # Create a form instance for Book 
        form = BookForm(data={
            'title': title,
            'author': author_name,
            #'published_date': first_publish_year,
            'isbn': first_isbn
        })
        print(form)

        save_and_create_owned_book(form, Book, request.user, commit=False)

    return render(request, 'books/search_book.html', {'results': results})


