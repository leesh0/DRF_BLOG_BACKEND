from django.db import models
from django.contrib.auth import get_user_model
from .utils.helpers import pk_gen
from uuid import uuid4
from taggit.managers import TaggableManager

User = get_user_model()


# Create your models here.
class Series(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='series')
    title = models.CharField(max_length=120, verbose_name='Series title')
    slug = models.SlugField(max_length=200, verbose_name='Series Slug',allow_unicode=True)
    description = models.TextField(max_length=150, verbose_name='description', null=True, default=None)


class Post(models.Model):
    title = models.CharField(max_length=120, verbose_name='Post title')
    slug = models.SlugField(max_length=200, verbose_name='title id',allow_unicode=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    series = models.ForeignKey(Series, related_name='post', null=True, on_delete=models.SET_NULL)
    body = models.TextField()
    description = models.TextField(max_length=150)
    thumbnail = models.CharField(max_length=30, default='📄')
    tags = TaggableManager(blank=True)
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_like')


class PostComment(models.Model):
    id = models.CharField(max_length=36, default=uuid4, unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name='reply')
    body = models.TextField(max_length=1500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
