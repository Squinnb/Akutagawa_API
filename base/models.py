from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    pass

    def __str__(self):
        return self.username

class Book(models.Model):
    author = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    year = models.CharField(max_length=5)
    magazine = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.title} by {self.author}"

    
class Review(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=30)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")

    def __str__(self):
        return f"{self.user.username} says this: {self.title}..."



