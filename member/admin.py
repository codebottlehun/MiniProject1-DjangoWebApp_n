from django.contrib import admin
from .models import User, Alarm


# Register your models here.
@admin.register(User)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(Alarm)
class PostAdmin(admin.ModelAdmin):
    pass