from django.urls import path
from . import views

app_name='codagram'
urlpatterns=[
    path('', views.index, name='index'),
    path('postlist_new/', views.postlist_new, name='postlist_new'),
    path('denine/', views.denine_404, name='denine_404'),
]