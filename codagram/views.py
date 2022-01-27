from datetime import timedelta
from django.shortcuts import render
from django.utils import timezone
from post.models import Post 
from member.views import my_paper
    
default_message = 'The page you are looking for might have been removed had its name changed or is temporarily unavailable.'
# Create your views here.
def index(request):
    timesince = timezone.now() - timedelta(days=3)
    #\.filter(created_at__gte=timesince)[:10]
    post_list = Post.objects.all()
    q = request.GET.get('q', '')
    if q:
        post_list = post_list.filter(subject__icontains=q)
        if not post_list.exists():
            return render(request, "codagram/denine_404.html", {
                "DontShowSide" : "Y",
                "main" : "SORRY!",
                "title" : "Not found in the database.",
                "message" : "There are no searched results. But, We'll try harder and help you find it someday.",
                })

    context = my_paper(request)
    context.update({"post_list":post_list})
    return render(request, "codagram/index.html", context)

def denine_404(request, title = "404 - Page not found", msg = default_message):
    message = msg
    title = title
    return render(request, "codagram/denine_404.html", {
        "title" : title,
        "message" : message,
        "btn" : "f",
    })

def post_new(request):
    return(request, "codagram/")
    pass