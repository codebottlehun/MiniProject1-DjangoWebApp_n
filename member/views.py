from django.shortcuts import render, redirect
from django.urls import is_valid_path
from importlib_metadata import email
from .models import User, Write, Comment
from .forms import SignupForm
from django.utils import timezone
from django.http import HttpResponse, request
from django.core.paginator import Paginator
from django.contrib.auth import login as auth_login

#bottle - django 
from django.contrib.auth.views import (
    LoginView, logout_then_login
)

login = LoginView.as_view(template_name="member/login_form.html")

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
    return logout_then_login(request)


def my_page(request) :
    # 내가 쓴 글 리스트업 작업
    wri_page = request.GET.get('wri_page', 1)

    #최신순 정렬이 필요해보입니다.

    id = request.session['user_name']
    write = Write.objects.filter(author = id)

    write_p = Paginator(write, 5)
    wri_info = write_p.page(wri_page)

    wri_start_page = (wri_page -1) //5 *5 + 1
    wri_end_page = wri_start_page + 4
    if wri_end_page > write_p.num_pages :
        wri_end_page = write_p.num_pages

    # 내가 쓴 글 리스트업 작업
    com_page = request.GET.get('com_page', 1)

    comment = Comment.objects.filter(author = id)

    com_p = Paginator(comment, 5)
    com_info = com_p.page(com_page)

    com_start_page = (com_page -1) //5 *5 + 1
    com_end_page = com_start_page + 4
    if com_end_page > com_p.num_pages :
        com_end_page = com_p.num_pages

    context = {
        'wri_info' : wri_info, 
        'wri_range' : range(wri_start_page, wri_end_page),
        'com_info' : com_info, 
        'com_range' : range(com_start_page, com_end_page)
    }

    return render(request, 'member/mypage.html', context)

def delete(request) :
    text_type = request.GET.get('text_type')
    id = request.GET.get('id')
    
    if text_type :
        data = Comment.objects.filter(id=id)
    else :
        data = Write.objects.filter(id=id)
    
    data.delete()

    return redirect('member:mypage')