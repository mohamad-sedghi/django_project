from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Book(models.Model):
   
    image = models.ImageField(upload_to='img/', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False)
    author = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False)
    publisher = models.CharField(max_length=100, null=False)
    translator = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    comments_count = models.IntegerField(default=0, null=False)
    likes = models.ManyToManyField(User, related_name='liked_books', blank=True)

    def __str__(self):
        return self.title  #for show in admin panel
    
    def likes_count(self):
        return self.likes.count()
   
    def get_absolute_url(self):
        return reverse("Book:book_detail", args=[self.pk]) # url book_detail 
    


class Comment(models.Model):
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, null=False, on_delete=models.CASCADE)
    text = models.TextField(null=False, blank=False)
    created_at = models.TimeField(auto_now_add=True)

