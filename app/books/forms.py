from django import forms
from . models import Book, OwnedBook, Shelf

# form for adding books manually
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'published_date', 'cover_image']    

#class ShelfForm(forms.ModelForm):
    #class Meta:
        #model = Shelf
        #fields = ['isbn', 'shelf']