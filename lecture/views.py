from django.shortcuts import render, redirect
from .models import Video,Memo, Question
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
    videos = Video.objects.all()
    memos = Memo.objects.all()
    return render(request, 'lecture/index.html', context={'videos':videos, 'memos':memos})

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
        model = MemoLecture.objects.all()
        text = ''
        for i in model:
            text += i.text + '\n'
        form = MemoForm(initial={'text' : text})
        return render(request, 'lecture/memo.html', {'f':form, 'memo':model})
    elif request.method == "POST":
        form = MemoForm(request.POST)
        # if form.is_valid():
        model = MemoLecture.objects.all()
        model.delete()
        q = form.save(commit=False)
        q.save()
        return HttpResponseRedirect(reverse('lecture:memo'))

'''
안씀
'''

def home(request):
    return render(request, 'home.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']
    
    if Room.objects.filter(name=room).exists():
        return redirect('lecture/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('lecture/'+room+'/?username='+username)
    
def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})