from django.http import HttpResponse, JsonResponse
from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.utils import timezone
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

def index(request):
    post_list = Post.objects.order_by('-register_date')
    context = { 'post_list': post_list }
    return render(request, 'post/post_list.html', context)

def detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = { 
        'post': post,
    }
    return render(
        request, 'post/post_detail.html', context)

def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    #author = request.GET.get('username')
    #c = Comment.objects.get(author=author)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            #comment.author = request.session['user_id'] JBH
            comment.author = request.user.username
            comment.register_date = timezone.now()
            comment.post = post
            comment.save()
            return redirect('post:detail', post_id=post.id)
    else:
        form = CommentForm()
    context = {'post': post, 'form': form}
    return render(request, 'post/comment_detail.html', context)

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            #post.author = request.session['user_id'] JBH
            post.author = request.user.username
            post.register_date = timezone.now()
            post.save()
            return redirect('post:index')
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'post/post_form.html', context)

def comment_get(request):
    author = request.GET.get('username')
    c = Comment.objects.get(author=author)
    data=[]
    d = model_to_dict(c)
    data.append(d)
    return JsonResponse(data, safe=False)