from datetime import timedelta
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from post.models import Post 
from member.views import my_paper, alarm
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.core.paginator import Paginator
import json
    
default_message = 'The page you are looking for might have been removed had its name changed or is temporarily unavailable.'
onepagecnt = 10

# Create your views here.
def index(request):
    post_list = {}
    q = request.GET.get('q', '')
    if q:
        post_list = Post.objects.filter(subject__icontains=q)[:onepagecnt]
        if not post_list.exists():
            return render(request, "codagram/denine_404.html", {
                "DontShowSide" : "Y",
                "main" : "SORRY!",
                "title" : "Not found in the database.",
                "message" : "There are no searched results. But, We'll try harder and help you find it someday.",
                })
    else:
        post_list = Post.objects.all()[:onepagecnt]

    context = my_paper(request)
    context.update({"post_list":post_list})

    source = alarm(request)
    data = json.loads(source.content)
    
    alarmlist = [];
    for i,c in enumerate(data):
        if i<10 :
            alarmlist.append(c)

    context.update({"alarm_list":alarmlist})

    if len(post_list) < onepagecnt:
        context.update({"more":"F"})

    return render(request, "codagram/index.html", context)

def denine_404(request, title = "404 - Page not found", msg = default_message):
    message = msg
    title = title
    return render(request, "codagram/denine_404.html", {
        "title" : title,
        "message" : message,
        "btn" : "f",
    })

@csrf_exempt
def postlist_new(request):
    page = json.loads(request.body)


    q = page.get('query', '')
    print(q)
    post_all = ''
    if q:
        post_all = Post.objects.filter(subject__icontains=q)
        print('검색')
    else:
        post_all = Post.objects.all()
        print('미검색')

    page_num = int(page.get('paging_list')) + 1

    paginator = Paginator(post_all, onepagecnt) 
    print(str(page_num) + "/" + str(paginator.num_pages))

    post_data = paginator.get_page(1).object_list
    if page_num < paginator.num_pages + 1:
        post_data = paginator.get_page(page_num).object_list
        more = "T"
        if page_num == paginator.num_pages:
            more = "F"
        return render(request, "codagram/new_list.html", {
            "post_list": post_data,
            "more": more,
        })

    return HttpResponse()