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

@login_required
def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author = request.user.username
    if request.method == 'POST':
        try:
            comment = Comment.objects.get(author=author)
            if request.method == "POST":
                if request.POST.get('content')!=None:
                    comment.content = request.POST.get('content')
                if request.POST.get('description')!=None:
                    comment.description = request.POST.get('description')
                if request.POST.get('content')!=None or request.POST.get('description')!=None:
                    comment.save()
                    return redirect('post:detail', post_id=post.id)
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
   
    # context = {'post': post, 'form': form}
    # return render(request, 'post/comment_detail.html', context)

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

@login_required
def post_update(request, post_id):
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
        context = {
            'form':form,
            'post':post,
        }
        return render(request, 'post/post_form_update.html', context)
    else:
        return redirect('post:detail', post_id=post.id)

@login_required
def post_delete(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('post:index')

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