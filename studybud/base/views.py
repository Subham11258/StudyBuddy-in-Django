from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from .models import Room,Topic,message,User
from .forms import RoomForm, UserForm, MyUserCreationForm

# Create your views here.
#rooms=[
 #   {"id":1,"name":"Let's learn Python"},
 #   {"id":2,"name":"Design with me"},
 #   {"id":3,"name":"Backend Development"}
#]
def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms=Room.objects.filter(Q(topic__name__icontains=q) |  Q(name__icontains=q) | Q(description__icontains=q))
    topic=Topic.objects.all()[0:5]
    room_count=rooms.count()
    roomMessages=message.objects.filter(Q(room__topic__name__icontains=q))
    context={'rooms':rooms,'topic':topic,'room_count':room_count,'roomMessages':roomMessages}
    return render(request,'home.html',context)
def room(request,pk):
    room=None
    room=Room.objects.get(id=pk)
    roomMessages=room.message_set.all()
    participants=room.participants.all()
    if request.method=='POST':
        roomMessages=message.objects.create(
        user=request.user,
        room=room,
        body=request.POST.get('body')
    )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    context={'room':room,'roomMessages':roomMessages,'participants':participants}        
    return render(request,'room.html',context)
def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    roomMessages=user.message_set.all()
    topic=Topic.objects.all()
    context={'user':user,'rooms':rooms,'roomMessages':roomMessages,'topic':topic}
    return render(request,'profile.html',context)
    
@login_required(login_url='/login')
def createRoom(request):
    form=RoomForm()
    topics=Topic.objects.all()
    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        
        return redirect('home')
    context={'form':form,'topics':topics}
    return render(request,'room_form.html',context)
@login_required(login_url='/login')
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    topics=Topic.objects.all()
    if request.user!=room.host:
        return HttpResponse('You are not allowed here!')
    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context={'form':form,'topics':topics,'room':room}
    return render(request,'room_form.html',context)
@login_required(login_url='/login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user!=room.host:
        return HttpResponse('You are not allowed here!')
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'delete.html',{'obj':room})
def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        username=request.POST.get('email')
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,"User does not exist") 
        user=authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or password does not exist')
    context={'page':page}
    return render(request,'login_register.html',context)
def registerPage(request):
    
    form=MyUserCreationForm()
    if request.method=='POST':
        form=MyUserCreationForm(request.POST)
        if form.is_valid():
            
            user=form.save(commit=False)
            
            user.save()
            auth.login(request,user)
            return redirect('/')
        else:
            messages.error(request,'An error occurred during registration')
    return render(request,'login_register.html',{'form':form})
def logoutUser(request):
    logout(request)
    return redirect('/')
@login_required(login_url='/login')
def deleteMessage(request,pk):
    Message=message.objects.get(id=pk)
    if request.user!=Message.user:
        return HttpResponse('You are not allowed here!')
    if request.method=='POST':
        Message.delete()
        return redirect('home')
    return render(request,'delete.html',{'obj':Message})

@login_required(login_url="/login")
def updateUser(request):
    user=request.user
    form=UserForm(instance=user)
    if request.method=='POST':
        form=UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=user.id)
    context={'form':form}
    return render(request,'update-user.html',context)
def topicsPage(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    topics=Topic.objects.filter(name__icontains=q)
    context={'topics':topics}
    return render(request,'topics.html',context)
def activityPage(request):
    roomMessage=message.objects.all()
    return render(request,'activity.html',{'roomMessage':roomMessage})