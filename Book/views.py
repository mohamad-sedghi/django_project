from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse ,get_object_or_404
from .models import Book, Comment
from .forms import UserCreationForm, LoginForm, CommentForm
from django.contrib.auth import authenticate, login, logout


def index(request):
    # گرفتن تمام کتاب‌ها از دیتابیس
    books = Book.objects.all()
    return render(request, 'index.html', {'books': books})


def register(request):
    # چک می‌کنیم که کاربر لاگین نکرده باشه
    if not request.user.is_authenticated:
        if request.method == 'POST':
            # ایجاد فرم ثبت‌نام با داده‌های POST
            form = UserCreationForm(request.POST)

            if form.is_valid():
                # اگر فرم معتبر بود، کاربر جدید رو ثبت می‌کنیم
                Register_user=User.objects.create_user(
                    username=form.cleaned_data.get('username'),
                    email=form.cleaned_data.get('email'),
                    password=form.cleaned_data.get('password')
                )
                # بعد از ثبت‌نام، کاربر رو لاگین می‌کنیم
                login(request, Register_user)
                return redirect('Book:index')  # انتقال به صفحه اصلی

            else:
                # اگر فرم اشتباه باشه، دوباره فرم رو با خطاها نشون می‌ده
                return render(request, 'sign_up.html', {'form': form})

        else:
            # اگر درخواست GET باشه، فرم خالی رو نمایش می‌ده
            form = UserCreationForm()

        return render(request, 'sign_up.html', {'form': form})
    else:
        return redirect('Book:index')  # اگر کاربر لاگین کرده، به صفحه اصلی هدایت می‌کنیم


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
                return redirect('Book:index')  # هدایت به صفحه اصلی
        else:
            # اگر اطلاعات اشتباه باشه، فرم رو دوباره با خطا نشون می‌ده
            return render(request, 'login.html', {'form': form})
    else:
        # درخواست GET: فرم خالی رو نشون می‌ده
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    # اگر کاربر وارد شده، او رو لاگ‌اوت می‌کنیم
    if request.user.is_authenticated:
        logout(request)
        return redirect('Book:index')
    else:
        return redirect('Book:login')


def book_detail(request, pk):
    # پیدا کردن کتاب با استفاده از pk
    book = Book.objects.get(id=pk)
    # گرفتن نظرات مرتبط با این کتاب
    comments = Comment.objects.filter(book=book)
    if request.method == 'POST':
        # اگر کاربر لاگین باشه، کامنت جدید رو ذخیره می‌کنیم
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                # ایجاد کامنت جدید
                comment = form.save(commit=False)
                comment.author = request.user  # نویسنده کامنت همون کاربر فعلی
                comment.book = book  # کتاب مرتبط
                comment.save()
                # به‌روز رسانی تعداد نظرات کتاب
                book.comments_count += 1 
                book.save()
                return redirect(reverse('Book:book_detail', args=[pk]))  # بازگشت به صفحه جزئیات کتاب
        else:
            return redirect('Book:login')  # اگر کاربر لاگین نکرده، به صفحه لاگین هدایت می‌شود
    else:
        if book is None:
            return redirect('Book:index')  # اگر کتاب پیدا نشد، به صفحه اصلی هدایت می‌کنیم
        else:
            form = CommentForm()
            return render(request, 'book_detail.html', {'book': book, 'comments': comments, 'form': form})


def delete_comment(request, pk):
    # پیدا کردن کامنت بر اساس pk
    comment = get_object_or_404(Comment, pk=pk)
    
    # بررسی اینکه آیا کاربر لاگین شده نویسنده کامنت هست یا نه
    if comment.author == request.user:
        comment.delete()  # اگر بله، کامنت رو حذف می‌کنیم
    
    # بعد از حذف کامنت، به صفحه جزئیات کتاب هدایت می‌کنیم
    return redirect('Book:book_detail', pk=comment.book.pk)
