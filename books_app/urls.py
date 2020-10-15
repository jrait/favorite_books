from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('home',views.home),
    path('register',views.register),
    path('login',views.login),
    path('logout',views.logout),
    path('add_book',views.add_book),
    path('books/<int:book_id>',views.book_info),
    path('update',views.update),
    path('delete/<int:book_id>',views.delete),
    path('books/<int:book_id>/like',views.like),
    path('books/<int:book_id>/dislike',views.dislike),
    path('liked_books',views.liked_books)
]