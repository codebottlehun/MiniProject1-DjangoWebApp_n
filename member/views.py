from django.shortcuts import render, redirect
from .models import Alarm
from post.models import Post, Comment
from .forms import SignupForm
from django.core.paginator import Paginator
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm

#bottle - django 
from django.contrib.auth.views import (
    LoginView, logout_then_login
)

def login(request) :
    if request.method == 'POST' :
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid() :
            auth_login(request, form.get_user())
            return redirect('codagram:index')
    else :
        form = AuthenticationForm()

    context = {
        'form' : form,
    }
    return render(request, 'member/login_form.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            auth_login(request, signed_user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = SignupForm()
    return render(request, 'member/signup_form.html', {
        'form': form,
    })

def logout(request) :
    return logout_then_login(request, login_url='')


def my_paper(request) :
    # 내가 쓴 글 리스트업 작업
    post_page = int(request.GET.get('wri_page', 1))

    id = request.user.get_username()
    post = Post.objects.filter(author = id)

    post.order_by('-register_date')

    post_p = Paginator(post, 5)
    post_data = post_p.page(post_page)

    post_start_page = (post_page -1) //10 *10 + 1
    post_end_page = post_start_page + 9
    if post_end_page > post_p.num_pages :
        post_end_page = post_p.num_pages

    # 내가 쓴 글 리스트업 작업
    com_page = request.GET.get('com_page', 1)

    comment = Comment.objects.filter(author = id)

    comment.order_by('-register_date')

    com_p = Paginator(comment, 5)
    com_data = com_p.page(com_page)

    com_start_page = (com_page -1) //5 *5 + 1
    com_end_page = com_start_page + 4
    if com_end_page > com_p.num_pages :
        com_end_page = com_p.num_pages

    context = {
        'post_data' : post_data, 
        'post_range' : range(post_start_page, post_end_page),
        'com_data' : com_data, 
        'com_range' : range(com_start_page, com_end_page),
        'post_page' : post_page, 
        'com_page' : com_page,
    }

    return context

def my_page(request) :
    # mypage에 들어갈 데이터 조회
    context = my_paper(request)

    return render(request, 'member/mypage.html', context)

def delete(request) :
    # mypage에서 댓글 삭제나 글 삭제 기능

    text_type = request.GET.get('text_type')
    id = request.GET.get('id')
    
    if text_type == "1" :
        data = Comment.objects.get(id=id)

    elif text_type == "0" :
        data = Post.objects.get(id=id)
    
    if data.author == request.user.get_username() :
        data.delete()

    return redirect('member:mypage')

def alarm(request) :
    # 사용자의 알람을 조회하는 기능
    alarm = Alarm.objects.filter(user = request.user.id)
    return alarm

def search(request, keyword) :
    # 검색 기능
    result = []
    for word in keyword.split(' ') :
        result.append(Post.objects.filter(subject__contains=word))
    return result