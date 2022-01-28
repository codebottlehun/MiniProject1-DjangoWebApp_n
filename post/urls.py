from django.urls import path, include
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:post_id>/', views.detail, name='detail'),
    path('post/create', views.post_create, name='post_create'),
    path('comment/create/<int:post_id>/', views.comment_create,  name='comment_create'),
    path('comment/delete/<int:post_id>/<str:author>/', views.comment_delete, name='comment_delete'),
    path('comment/select/<int:post_id>/<str:author>/', views.select_comment, name='select_comment'),
    path('comment/get/', views.comment_get, name='comment_get'),
    path('post/update/<int:post_id>', views.post_update, name='post_update'),
    path('post/delete/<int:post_id>', views.post_delete, name='post_delete'),
    path('post/like/<int:post_id>', views.like_post, name="like_post"),
    path('post/dislike/<int:post_id>/', views.dislike_post, name="dislike_post"),
]
