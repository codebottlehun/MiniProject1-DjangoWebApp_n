from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import resolve_url 
from post.models import Post, Comment

class User(AbstractUser) :
    # user_type select opsion
    NATIONAL_CHOICES = (
		(0, 'Aibler'),
        (1, 'Tutor'),
    )
    user_type = models.IntegerField(choices=NATIONAL_CHOICES, default=0) # user_type select form
    nickname = models.CharField(blank=True, max_length=50)
    user_photo = models.ImageField(blank=True)
    @property
    def user_photo_url(self):
        if self.user_photo:
            return self.user_photo.url
        else:
            return resolve_url("pydenticon_image", self.username)

class Alarm(models.Model) :
    write = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_time = models.DateTimeField(blank=True)
