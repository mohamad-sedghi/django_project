from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    image = models.ImageField(upload_to='img/', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False)
    author = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False)
    publisher = models.CharField(max_length=100, null=False)
    translator = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    # comments = models.ManyToManyField(Comment)
    comments_count = models.IntegerField(default=0, null=False)

    def __str__(self):
        return self.title
