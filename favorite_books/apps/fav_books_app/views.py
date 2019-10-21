from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "fav_books_app/index.html")

def registration(request):
    errors = User.objects.basic_validator(request.POST)
    request.session['email'] = request.POST['email']
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags='register')
        return redirect('/')
    else:
        password = request.POST['password']
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        
        new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], dob=request.POST['dob'], email=request.POST['email'], password=hashed_pw)
        new_user.save()

        return redirect('/books')
    

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags='login')
        return redirect('/')
    else: 
        user_from_db = User.objects.get(email=request.POST['email_login'])
        logged_user = user_from_db
        if bcrypt.checkpw(request.POST['password_login'].encode(), logged_user.password.encode()):
            request.session['email'] = logged_user.email
            return redirect('/books')
        else:
            return redirect('/')

def welcome(request):
    if "email" not in request.session:
        return redirect('/')
    else:
        context = {
            "this_user": User.objects.get(email=request.session['email']),
            "all_books": Book.objects.all(),
        }
        return render(request, "fav_books_app/add_book.html", context)

#-----books section---------------

def add_book(request):
    #form sends here....include validations here in the processing..
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags='books')
        return redirect('/books')
    else:    
        this_user = User.objects.get(email=request.session['email'])
        new_book = Book.objects.create(title=request.POST['book_title'], description=request.POST['book_description'], uploaded_by=this_user)
        new_book.users_liked.add(this_user)
        return redirect('/books')

def book_profile(request, book_id):
    context = {
        "this_user": User.objects.get(email=request.session['email']),
        "this_book": Book.objects.get(id=book_id),
        "all_books": Book.objects.all(),
    }
    return render(request, 'fav_books_app/book_profile.html', context)

def add_to_my_favs(request, book_id):
    this_user = User.objects.get(email=request.session['email'])
    this_book = Book.objects.get(id=book_id)
    this_book.users_liked.add(this_user)
    this_book.save()
    return redirect('/books/' + book_id)

def update_book(request, book_id):
    this_book = Book.objects.get(id=book_id)
    this_book.title = request.POST['edit_title']
    this_book.description = request.POST['edit_description']
    this_book.save()
    return redirect('/books')

def unfavorite(request, book_id):
    this_user = User.objects.get(email=request.session['email'])
    this_book = Book.objects.get(id=book_id)
    this_book.users_liked.remove(this_user)
    this_book.save()
    return redirect('/books/' + book_id)

def delete(request, book_id):
    this_book = Book.objects.get(id=book_id)
    this_book.delete()
    return redirect('/books')

def logout(request):
    request.session.clear()
    return redirect('/')
