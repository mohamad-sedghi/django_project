from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse ,get_object_or_404
from .models import Book, Comment
from django.http import JsonResponse
from .forms import UserCreationForm, LoginForm, CommentForm , BookForm
from django.contrib.auth import authenticate, login, logout


def index(request):
    # گرفتن تمام کتاب‌ها از دیتابیس
    books = Book.objects.all()
    return render(request, 'index.html', {'books': books})


def register(request):
    # چک می‌کنیم که کاربر لاگین نکرده باشه
    if not request.user.is_authenticated:
        if request.method == 'POST':
       
            form = UserCreationForm(request.POST) # گرفتن داده از فرم

            if form.is_valid():
                # کاربر جدید رو ثبت
                Register_user=User.objects.create_user(
                    username=form.cleaned_data.get('username'),
                    email=form.cleaned_data.get('email'),
                    password=form.cleaned_data.get('password')
                )
                # بعد از ثبت‌نام، کاربر رو لاگین می‌کنیم
                login(request, Register_user)
                return redirect('Book:index')  # بعدشم ریدایرکت به صفجه اول

            else:
                #فرم رو دوباره با خطا نشون 
                return render(request, 'sign_up.html', {'form': form})

        else:
           
            form = UserCreationForm()

        return render(request, 'sign_up.html', {'form': form})#فرم رو دوباره با خطا نشون 
    else:
        return redirect('Book:index')  


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            person = authenticate(request, username=username, password=password)
            if person is not None: 
                # اگر کاربر معتبر بود، لاگینش می‌کنیم
                login(request, person)
                return redirect('Book:index')  
        else:
            #فرم رو دوباره با خطا نشون 
            return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
  
    if request.user.is_authenticated:# کاربرلاگین بود 
        logout(request)# لاگاوت بعد ریدایرکت
        return redirect('Book:index')
    else:
        return redirect('Book:login')


def book_detail(request, pk):
    # pk پیدا کردن کتاب با استفاده از 
    book = Book.objects.get(id=pk)
    comments = Comment.objects.filter(book=book) # کامنت های کتاب
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                # ایجاد کامنت جدید
                comment = form.save(commit=False)
                comment.author = request.user  
                comment.book = book  
                comment.save()
              
                book.comments_count += 1 
                book.save()
                return redirect(reverse('Book:book_detail', args=[pk]))  # برگشت به جزئیات کتاب
        else:
            return redirect('Book:login')  
    else:
        if book is None:
            return redirect('Book:index')  
        else:
            form = CommentForm()
            return render(request, 'book_detail.html', {'book': book, 'comments': comments, 'form': form})


def delete_comment(request, pk):
    #pkپیدا کردن کامنت بر اساس 
    comment = get_object_or_404(Comment, pk=pk)
    
    #چک کاربر لاگین شده همون نویسنده کامنت هست یا نه
    if comment.author == request.user:
        comment.delete()  
    
   
    return redirect('Book:book_detail', pk=comment.book.pk)




def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
      
            book = form.save(commit=False)
            book.user = request.user 
            book.save()
            return redirect('Book:index') 
    else:
        form = BookForm()
    
    return render(request, 'add_book.html', {'form': form})




def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.user != request.user: #diffrent user
        return redirect('Book:book_detail', pk=pk)  

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book) # فایل واسه عکس کتابه
        if form.is_valid():
            form.save()
            return redirect('Book:book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    
    return render(request, 'edit_book.html', {'form': form, 'book': book})



def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.user == request.user:
        book.delete()
    return redirect('Book:index')  




def toggle_like(request, pk):
    if request.user.is_authenticated:  
        book = Book.objects.get(pk=pk)
        if request.user in book.likes.all():
            # اگر کاربر قبلاً لایک کرده بود، لایک را حذف می‌کنیم
            book.likes.remove(request.user)
        else:
            # اگر کاربر لایک نکرده بود، لایک را اضافه می‌کنیم
            book.likes.add(request.user)

        return redirect('Book:book_detail', pk=book.pk)
    else:
        return redirect('Book:login')  
