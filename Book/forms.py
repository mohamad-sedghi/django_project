from django import forms
from django.contrib.auth.models import User
from .models import Comment
from django.contrib.auth import authenticate
from .models import Book



class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='تکرار رمز عبور')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        # استایل‌ها رو برا فیلدا مشخص کردیم
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():  # اگه تکراری بود
            raise forms.ValidationError('این نام‌کاربری قبلاً انتخاب شده.')  
        return username

  
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():  # اگه تکراری بود
            raise forms.ValidationError('این ایمیل قبلاً ثبت شده.')  
        return email


    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:  # اگه یکی نبودن اینو می‌زنیم
            raise forms.ValidationError('رمز عبور و تکرارش یکی نیستن!')  
        return password2

    # ذخیره اطلاعات کاربر
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  
        if commit:
            user.save()
        return user


# فرم ورود به حساب کاربری
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام کاربری'
        }),
        label='نام کاربری'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور'
        }),
        label='رمز عبور'
    )

    # بررسی صحت اطلاعات وارد شده
    def clean(self):
        cleaned_data = super().clean()  
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        #username و password چک کردن
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('نام کاربری یا رمز عبور اشتباهه')  
        return cleaned_data


# فرم ارسال کامنت
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']  
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'نظر خودتو اینجا بنویس...',
                'rows': 4
            })
        }
        labels = {
            'text': 'متن نظر:',
        }

        # فیلدهای مخفی برای اطلاعات کتاب و نویسنده کامنت
        book = forms.CharField(widget=forms.HiddenInput(), required=False)
        author = forms.CharField(widget=forms.HiddenInput(), required=False)



class BookForm(forms.ModelForm): # واسه اد بوک
    class Meta:   
        model = Book
        fields = ['title', 'author', 'description', 'publisher', 'translator', 'image']

