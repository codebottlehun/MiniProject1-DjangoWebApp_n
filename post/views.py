from django.http import HttpResponse, JsonResponse
from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.utils import timezone
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from member.views import alarm
import json

def index(request):
    post_list = Post.objects.order_by('-register_date')
    context = { 'post_list': post_list }
    return render(request, 'post/post_list.html', context)

def detail(request, post_id):
    # Alarm info. JBH
    context = {}
    source = alarm(request)
    data = json.loads(source.content)
    
    alarmlist = [];
    for i,c in enumerate(data):
        if i<100 :
            alarmlist.append(c)

    context.update({"alarm_list":alarmlist})

    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post_id=post_id).order_by("-choice")
    context.update({ 
        'post': post,
        'comments':comments,
    })
    return render(
        request, 'post/post_detail.html', context)

@login_required
def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author = request.user.username
    if request.method == 'POST':
        context = {}
        source = alarm(request)
        data = json.loads(source.content)
        
        alarmlist = [];
        for i,c in enumerate(data):
            if i<100 :
                alarmlist.append(c)

        context.update({"alarm_list":alarmlist})
        try:
            comment = post.comment_set.get(author=author)
            if request.method == "POST":
                if request.POST.get('content')!=None:
                    comment.content = request.POST.get('content')
                if request.POST.get('description')!=None:
                    comment.description = request.POST.get('description')
                if request.POST.get('content')!=None or request.POST.get('description')!=None:
                    comment.save()
                    return redirect('codagram:index', context)
        except:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.author = request.user.username
                comment.register_date = timezone.now()
                comment.post = post
                comment.save()
                return redirect('post:detail', post_id=post.id)
    else:
        form = CommentForm()


@login_required
def post_create(request):

    # Alarm info. JBH
    context = {}
    source = alarm(request)
    data = json.loads(source.content)
    
    alarmlist = [];
    for i,c in enumerate(data):
        if i<100 :
            alarmlist.append(c)

    context.update({"alarm_list":alarmlist})

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            #post.author = request.session['user_id'] JBH
            post.author = request.user.username
            post.register_date = timezone.now()
            post.save()

            # tags = form.cleaned_data['tags'].split(',')
            # for tag in tags:
            #     if not tag:
            #         continue
            #     tag = tag.strip()
            #     _tag, _ = Tag.objects.get_or_create(name=tag)

            #     post.tags += _tag
            return redirect('codagram:index')
    else:
        form = PostForm()
    context.update({'form': form}) 
    return render(request, 'post/post_form.html', context)

@login_required
def post_update(request, post_id):
    # Alarm info. JBH
    context = {}
    source = alarm(request)
    data = json.loads(source.content)
    
    alarmlist = [];
    for i,c in enumerate(data):
        if i<100 :
            alarmlist.append(c)

    context.update({"alarm_list":alarmlist})

    post = get_object_or_404(Post, id=post_id)
    if post.author == request.user.username:
        if request.method == 'POST':
                try:
                    post.subject = request.POST.get('subject')
                    post.description = request.POST.get('description')
                    post.content = request.POST.get('content')
                    post.save()
                    return redirect('post:detail', post_id=post.id)  
                except:
                    return render(request, 'post:post_update', post_id=post.id)
            
        form = PostForm(initial={'subject':post.subject, 'description':post.description, 'content':post.content})
        context.update({
            'form':form,
            'post':post,
        })
        return render(request, 'post/post_form_update.html', context)
    else:
        return redirect('post:detail', post_id=post.id)

@login_required
def post_delete(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('codagram:index')

def comment_get(request):
    author = request.GET.get('username')
    c = Comment.objects.get(author=author)
    data=[]
    d = model_to_dict(c)
    data.append(d)
    return JsonResponse(data, safe=False)

def comment_delete(request, post_id, author):
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.get(author=author)
    comment.delete()
    return redirect('post:detail', post_id=post.id)

def select_comment(request, post_id, author):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, author=author)
    if request.method=="POST":
        post.solved = True
        post.save()
        comment.choice = True
        comment.save()
    return redirect('post:detail', post_id=post.id)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.likes.add(request.user)
    messages.success(request, "해당 게시물에 좋아요를 눌렀습니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)


@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.likes.remove(request.user)
    messages.success(request, "해당 게시물에 좋아요를 취소하였습니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)