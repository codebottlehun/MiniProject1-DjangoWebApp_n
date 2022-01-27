from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from django_pydenticon.views import image as pydenticon_image

urlpatterns = [
    #project app
    path('admin/', admin.site.urls),
    path('codagram/', include('codagram.urls')),
    path('member/', include('member.urls')),
    path('post/', include('post.urls')),
    path('lecture/', include('lecture.urls')), #lecture
    
    path('identicon/image/<path:data>/', pydenticon_image, name='pydenticon_image'),
    path('', RedirectView.as_view(pattern_name='codagram:index')),
    path('accounts/login/', RedirectView.as_view(pattern_name='codagram:index')), # logout
    re_path('', RedirectView.as_view(pattern_name='codagram:denine_404')),
    
]
