from django.urls import path, include
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:post_id>/', views.detail, name='detail'),
    path('post/create', views.post_create, name='post_create'),
    path('comment/create/<int:post_id>/', views.comment_create,  name='comment_create'),
    path('comment/get/', views.comment_get),
    path('post/update/<int:post_id>', views.post_update, name='post_update'),
]
