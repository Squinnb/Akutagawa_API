from django.contrib import admin
from .models import User, Book, Review

admin.site.register(User)
admin.site.register(Book)
admin.site.register(Review)
# Register your models here.
