from django.shortcuts import render
from member.views import my_paper # profile.html 값을 저장하고 있는 함수

# Create your views here.
def index(request):
    #timesince = timezone.now() - timedelta(days=3)
    #Post Model
    #post_list = Post.objects.all()
    context = my_paper(request) # profile.html 값을 저장하고 있는 함수(member.view) Jeon_SH
    return render(request, "codagram/index.html", context)

def post_new(request):
    return(request, "codagram/")
    pass