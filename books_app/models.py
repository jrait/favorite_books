from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def register_validator(self,postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name'])<2:
            errors['first_name'] = "First name must be at least 2 characters"
        if len(postData['last_name'])<2:
            errors['last_name'] = "Last name must be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['first_name'] = "Please enter a valid email"
        if len(postData['password'])<8:
            errors['password'] = "Password must be at least 8 characters"
        if postData['password'] != postData ['password_confirm']:
            errors['password_match'] = "Passwords do not match"
        return errors

class BookManager(models.Manager):
    def book_validator(self,postData):
        errors = {}
        if len(postData['title'])<1:
            errors['title'] = "Book must include a title"
        if len(postData['desc'])<5:
            errors['desc'] = "Book description must be greater than 5 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.CharField(max_length = 45)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    # books_uploaded
    # books_liked

class Book(models.Model):
    title = models.CharField(max_length = 255)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    uploaded_by = models.ForeignKey(User,related_name = 'books_uploaded',on_delete = models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name = 'books_liked')
    objects = BookManager()