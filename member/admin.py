from django.contrib import admin
from .models import User, Write, Comment


# Register your models here.
@admin.register(User)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(Write)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class PostAdmin(admin.ModelAdmin):
    pass