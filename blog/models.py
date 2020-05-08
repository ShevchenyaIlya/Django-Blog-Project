from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    likes_number = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    article = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField('Comment text', max_length=200)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment_text
