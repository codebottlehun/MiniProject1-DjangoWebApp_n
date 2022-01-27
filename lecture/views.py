from django.shortcuts import render, redirect
from .models import Video, Question
from django.views.decorators.clickjacking import xframe_options_exempt
from django.shortcuts import render, get_object_or_404
from .models import Question, Choice
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from .forms import QuestionForm, ChoiceForm, VideoForm, MemoForm
from datetime import datetime
from .models import Room,Message,MemoLecture
from django.http import HttpResponse, JsonResponse

# Create your views here.

'''
video 관련 view
'''

def index(request):
    videos_tuttor = Video.objects.filter(user_type=1)
    videos_aibler = Video.objects.filter(user_type=0)
    return render(request, 'lecture/index.html', context={'video_tuttor':videos_tuttor, 'videos_aibler':videos_aibler})

def empty_page(request):
    return HttpResponse('lecture/empty_page.html')

def input_video(request):
    if request.method == "GET": 
        form = VideoForm()
        return render(request, 'lecture/input_video.html', {'f':form})
    elif request.method == "POST":
        form = VideoForm(request.POST)
        if form.is_valid():
            q = form.save(commit=False)

            '''
            url 입력시 embed url로 변환
            '''
            tmp_q = q.url
            tmp_q_spl = tmp_q.split('youtu.be')
            try:
                q.url = tmp_q_spl[0]+"youtube.com/embed"+tmp_q_spl[1]

                q.save()
            except:
                return HttpResponseRedirect(reverse('lecture:input_video'))
            return HttpResponseRedirect(reverse('lecture:input_video'))

'''
투표 관련 view
'''

def vote_index(request):
    a = Question.objects.all()
    return render(request, 'lecture/vote_index.html',{'a':a})

def detail(request, qid):
    b=get_object_or_404(Question, id=qid)
    return render(request, 'lecture/vote_detail.html',{'q':b})

def vote(request):
    if request.method == "POST" :
        c_id = request.POST.get('a')
        c = get_object_or_404(Choice, id = c_id) 
        c.votes += 1
        c.save() 
        return HttpResponseRedirect( reverse('lecture:result',args=(c.q.id ,)  ) )

def result(request, q_id):
    return render(request, 'lecture/vote_result.html', {'q' : get_object_or_404(Question, id = q_id) } )

def qregister(request):
    if request.method == "GET": 
        form = QuestionForm()
        return render(request, 'lecture/vote_qregister.html', {'f':form})
    elif request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = form.save(commit=False)
            q.date = datetime.now()
            q.save()
            return HttpResponseRedirect(reverse('lecture:vote_index'))

def qdelete(request, q_id):
    q = get_object_or_404(Question, id=q_id)
    q.delete()
    return HttpResponseRedirect(reverse('lecture:vote_index'))

def cregister(request):
    if request.method == "GET":
        form = ChoiceForm()
        return render(request, 'lecture/vote_cregister.html',{'f':form} )
    elif request.method == "POST":
        form = ChoiceForm(request.POST)
        if form.is_valid():
            c = form.save()
            # return HttpResponseRedirect(reverse('vote:detail', args=(c.q.id,)))
            # return HttpResponseRedirect(reverse('vote:index'))
            return HttpResponseRedirect(reverse('lecture:cregister'))
        else: 
            return render(request, 'lecture/vote_cregister.html',{'f':form, 'error':'유효하지않은 값입니다'})

def cdelete(request, c_id):
    c = get_object_or_404(Choice, id=c_id)
    c.delete()
    return HttpResponseRedirect(reverse('lecture:detail', args=(c.q.id, )))

'''
chat
'''

@xframe_options_exempt
def chat_room(request):
    return render(request, 'lecture/chat_room.html', {
    'room_name': 1,
})

'''
메모 관련 view
'''
def memo(request):
    if request.method == "GET": 
        try:
            model = MemoLecture.objects.get(user=request.user)
        except MemoLecture.DoesNotExist :
            model = MemoLecture.objects.create(user=request.user)

        # text = ''
        # for i in model:
        #     text += i.text + '\n'
        form = MemoForm(initial={'text' : model.text})
        return render(request, 'lecture/memo.html', {'f':form})
    elif request.method == "POST":
        form = MemoForm(request.POST)
        if form.is_valid():
            model = MemoLecture.objects.get(user=request.user)
            model.delete()  
            q = form.save(commit=False)
            q.user = request.user
            q.save()
        return HttpResponseRedirect(reverse('lecture:memo'))