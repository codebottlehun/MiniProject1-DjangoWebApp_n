from django.urls import path
from member import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'member'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('mypage/', views.my_page, name='mypage'),
    path('delete/', views.delete, name='delete'),
    path('alarm/', views.alarm, name='alarm'),
    path('check_alarm/', views.check_alarm, name='check_alarm'),
    path('click_alarm/', views.click_alarm, name='click_alarm'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)