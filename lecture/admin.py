from django.contrib import admin

from .models import Video,Question,Choice,Room,Message,MemoLecture

from embed_video.admin import AdminVideoMixin

class AdminVideo(AdminVideoMixin, admin.ModelAdmin):
    pass

class AdminMemo(AdminVideoMixin, admin.ModelAdmin):
    pass

admin.site.register(Video, AdminVideo)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(MemoLecture)