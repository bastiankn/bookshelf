from django.db import models
from django.contrib.auth.models import User

class Shelf(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100, blank=True)
    isbn = models.CharField(max_length=13, blank=True, unique=True)
    description = models.TextField(blank=True)
    published_date = models.DateField(null=True, blank=True)
    added_date = models.DateField(auto_now_add=True)
    #cover_image = models.ImageField(upload_to='book_covers/', blank=True)   
    
    def __str__(self):
        return self.title

class OwnedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isbn = models.ForeignKey(Book, on_delete=models.CASCADE)
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'"{self.isbn.title}" owned by {self.user.username}'

