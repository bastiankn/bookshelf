from django.db import models
from django.contrib.auth.models import User

# Predefined list of genres
GENRE_CHOICES = [
    ('fantasy', 'Fantasy'),
    ('sci-fi', 'Sci-Fi'),
    ('romance', 'Romance'),
    ('mystery', 'Mystery'),
    ('thriller', 'Thriller'),
    ('non-fiction', 'Non-Fiction'),
    ('horror', 'Horror'),
    ('historical', 'Historical'),
    ('biography', 'Biography'),
    ('poetry', 'Poetry'),
]

# Predefined list of statuses
STATUS_CHOICES = [
    ('unread', 'Unread'),
    ('reading', 'Currently Reading'),
    ('read', 'Read'),
    ('dtf', 'Didn`t Finish'),
]

class Shelf(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Tag(models.Model):
    tag = models.CharField(max_length=15, blank=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.tag

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100, blank=True)
    isbn = models.CharField(max_length=13, blank=True, unique=True)
    description = models.TextField(blank=True)
    published_date = models.DateField(null=True, blank=True)
    added_date = models.DateField(auto_now_add=True)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True) 
    
    def __str__(self):
        return self.title

class OwnedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isbn = models.ForeignKey(Book, on_delete=models.CASCADE)
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE, null=True, blank=True)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unread')
    rating = models.PositiveSmallIntegerField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def save(self, *args, **kwargs):
        if self.status == 'dtf':
            self.rating = 0
        elif self.status != 'read':
            self.rating = None
        super().save(*args, **kwargs)


    def __str__(self):
        return f'"{self.isbn.title}" owned by {self.user.username}'