from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from django_pydenticon.views import image as pydenticon_image

urlpatterns = [
    #Debug
    path('admin/', admin.site.urls),
    path('codagram/', include('codagram.urls')),
    path('member/', include('member.urls')),
    path('post/', include('post.urls')),
    re_path('', RedirectView.as_view(pattern_name='codagram:index'), name='root'),
    path('identicon/image/<path:data>/', pydenticon_image, name='pydenticon_image'),

    #project app
]
