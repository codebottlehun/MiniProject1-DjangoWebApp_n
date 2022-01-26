from django.urls import path
from . import views

app_name='codagram'
urlpatterns=[
    path('', views.index, name='index'),
    path('denine/', views.denine_404, name='denine_404'),
]