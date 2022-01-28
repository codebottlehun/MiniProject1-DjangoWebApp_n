from django.urls import path
from .views import *

app_name = 'lecture'

urlpatterns = [
    path('',index, name='index'),
    path('empty_page/',empty_page, name='empty_page'),
    path('input_video/',input_video,name='input_video'),
    
    # vote url
    path('index/', vote_index, name='vote_index'),
    path('<int:qid>', detail, name='detail'),
    path('qr', qregister, name='qregister'),
    path('vote/<int:q_id>/', vote, name='vote'),
    path('result/<int:q_id>/', result, name="result"),
    path('qd<int:q_id>', qdelete, name='qdelete'),
    path('cr/', cregister, name='cregister'),
    path('cd<int:c_id>', cdelete, name='cdelete'),

    # chat
    path('chat/', chat_room, name='chat'),

    # memo
    path('memo/', memo, name='memo'),
    ]
