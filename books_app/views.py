from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request,'index.html')

def home(request):
    if 'userid' in request.session:
        context = {
            'user':User.objects.get(id = int(request.session['userid'])),
            'all_books':Book.objects.all(),
        }
        return render(request,'dashboard.html',context)
    return redirect('/')

def register(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors)>0:
            for key,value in errors.items():
                messages.error(request,value)
            return redirect('/')
        else:
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
            User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password = pw_hash
            )
            request.session['userid'] = User.objects.last().id
            return redirect('/home')
    return redirect('/')

def login(request):
    user = User.objects.filter(email = request.POST['login_email'])
    if user: 
        if bcrypt.checkpw(request.POST['login_password'].encode(),user[0].password.encode()):
            request.session['userid'] = user[0].id
            return redirect('/home')
    messages.error(request,"Email or Password is Invalid")
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def add_book(request):
    if request.method == "POST":
        errors = Book.objects.book_validator(request.POST)
        if len(errors)>0:
            for key,value in errors.items():
                messages.error(request,value)
        else:
            Book.objects.create(
                title = request.POST['title'],
                desc = request.POST['desc'],
                uploaded_by = User.objects.get(id = int(request.session['userid']))
            )
            Book.objects.last().liked_by.add(User.objects.get(id = int(request.session['userid'])))
    return redirect('/home')

def book_info(request,book_id):
    context = {
        'book': Book.objects.get(id = book_id),
        'user' : User.objects.get(id = int(request.session['userid']))
    }
    return render(request,'book_info.html',context)

def update(request):
    book_to_update = Book.objects.get(id = int(request.POST['book_id']))
    if request.method == "POST":
        errors = Book.objects.book_validator(request.POST)
        if len(errors)>0:
            for key,value in errors.items():
                messages.error(request,value)
        else:
            book_to_update.title = request.POST['title']
            book_to_update.desc = request.POST['desc']
            book_to_update.save()
    return redirect(f'/books/{book_to_update.id}')

def delete(request,book_id):
    book_to_delete = Book.objects.get(id = book_id)
    book_to_delete.delete()
    return redirect('/home')

def like(request,book_id):
    book_to_like = Book.objects.get(id = book_id)
    user = User.objects.get(id = int(request.session['userid']))
    book_to_like.liked_by.add(user)
    return redirect(f'/books/{book_id}')

def dislike(request,book_id):
    book_to_unlike = Book.objects.get(id = book_id)
    user = User.objects.get(id = int(request.session['userid']))
    book_to_unlike.liked_by.remove(user)
    return redirect('/home')

def liked_books(request):
    if 'userid' in request.session:
        context = {
            'user':User.objects.get(id = int(request.session['userid'])),
            'all_books':Book.objects.all(),
        }
        return render(request,'liked_books.html',context)
    return redirect('/')