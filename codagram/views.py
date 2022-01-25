from django.shortcuts import render

# Create your views here.
def index(request):
    #timesince = timezone.now() - timedelta(days=3)
    #Post Model
    #post_list = Post.objects.all()
    return render(request, "codagram/index.html",{})

def post_new(request):
    return(request, "codagram/")
    pass