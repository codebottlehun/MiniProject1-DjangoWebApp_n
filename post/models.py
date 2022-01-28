from email.policy import default
from django.db import models
from ckeditor.fields import RichTextField
from tagging.fields import TagField
from django.conf import settings

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    author = models.CharField(max_length=200, default=None)
    subject = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    content = RichTextField()
    register_date = models.DateTimeField()
    solved = models.BooleanField(default=False)
    tag = TagField()
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_posts", blank=True)

    def __str__(self):
        return self.subject

    @property
    def get_comment_cnt(self):

        cmt_cnt = Comment.objects.filter(post = self.pk)

        return len(cmt_cnt)

    class Meta:
        ordering=['-register_date']


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    author = models.CharField(max_length=200, default=None)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    register_date = models.DateTimeField()
    choice = models.BooleanField(default=False)
    check = models.BooleanField(default=False)