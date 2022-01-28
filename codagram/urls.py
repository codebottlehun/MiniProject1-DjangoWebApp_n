from django.urls import path
from . import views

app_name='codagram'
urlpatterns=[
    path('', views.index, name='index'),
    path('postlist_new/', views.postlist_new, name='postlist_new'),
    path('reset_alarm/', views.reset_alarm, name='reset_alarm'),
    
    path('denine/', views.denine_404, name='denine_404'),

]