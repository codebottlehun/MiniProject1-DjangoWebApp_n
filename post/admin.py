from django.contrib import admin

# Register your models here.
from .models import Post, Comment


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class PostAdmin(admin.ModelAdmin):
    pass