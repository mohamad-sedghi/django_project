from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Book
from .forms import UserCreationForm, LoginForm
from django.contrib.auth import authenticate, login, logout


def index(request):
    books = Book.objects.all()
    return render(request, 'index.html', {'books': books})


def register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            # ایجاد فرم با داده‌های POST
            form = UserCreationForm(request.POST)

            if form.is_valid():
                # ذخیره کاربر جدید در صورت اعتبار فرم
                User.objects.create_user(
                    username=form.cleaned_data.get('username'),
                    email=form.cleaned_data.get('email'),
                    password=form.cleaned_data.get('password')
                )
                return redirect('Book:login')  # مسیر لاگین

            else:
                # فرم نامعتبر است؛ داده‌های فرم همراه خطاها به قالب ارسال می‌شود
                return render(request, 'sign_up.html', {'form': form})

        # درخواست GET: نمایش فرم خالی
        else:
            form = UserCreationForm()

        return render(request, 'sign_up.html', {'form': form})
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
                # کاربر معتبر است، او را لاگین کن
                login(request, person)
                return redirect('Book:index')  # تغییر مسیر به صفحه اصلی یا دلخواه
            else:
                # نام‌کاربری یا رمز عبور اشتباه است
                return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('Book:index')
    else:
        return redirect('Book:login')
