from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils.helpers import upload_avatar_to


# Create your models here.
class BodeUser(AbstractUser):
    nickname = models.CharField(max_length=15, default=None, null=True)
    introduce = models.TextField(max_length=100, default=None, null=True)
    blog_name = models.CharField(max_length=15, default=None, null=True)
    avatar = models.ImageField(upload_to=upload_avatar_to, verbose_name='avatar', default=None, null=True)
    twitter = models.CharField(max_length=15, default=None, null=True)
    github = models.CharField(max_length=39, default=None, null=True)

    def save(self, *args, **kwargs):
        try:
            this = BodeUser.objects.get(id=self.id)
            if this.avatar != self.avatar:
                this.avatar.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super().save(*args, **kwargs)


class RegistrationMailModel(models.Model):
    email = models.EmailField(
        unique=True,
        verbose_name='email id',
        max_length=100,
        help_text="EMAIL for Wait"
    )
    key = models.CharField(max_length=200, verbose_name='register key', unique=True)
    activated = models.BooleanField(verbose_name='is activated', default=False)
    expire = models.DateTimeField(verbose_name='expire')
