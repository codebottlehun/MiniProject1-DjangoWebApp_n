from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView

urlpatterns = [
    #Debug
    path('admin/', admin.site.urls),
    path('codagram/', include('codagram.urls')),
    path('member/', include('member.urls')),
    re_path('', RedirectView.as_view(pattern_name='codagram:index'), name='root'),

    #project app
]
