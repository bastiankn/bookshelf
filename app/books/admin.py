from django.contrib import admin
from .models import Shelf, Book, OwnedBook

# Register your models here.
admin.site.register(Shelf)
admin.site.register(Book)
admin.site.register(OwnedBook)