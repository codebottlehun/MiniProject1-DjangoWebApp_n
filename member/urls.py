from django.urls import path
from member import views

app_name = 'member'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('mypage/', views.my_page, name='mypage'),

]