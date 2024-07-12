from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room, Topic, Message
from django.contrib.auth.decorators import login_required
from .forms import RoomForm,UserForm
from django.db.models import  Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate, logout
from django.contrib import  messages
# from django.http import HttpResponse

# rooms=[
#     {'id':1,'name': "Lets learn python!"},
#     {'id':2,'name': "design with me"},
#     {'id':3,'name': "front-end developer"},
# ]
def loginPage(request):
    page ='login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user=User.objects.get(username = username)
        except:
            messages.error(request, "no username exists.")
            
            
            
        user = authenticate(request,username=username, password = password)
        print(user)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        
        else:
            messages.error(request, "username or password doesn't exist")
    context={'page':page}
    return render(request, 'base/login_register.html',context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    page = 'register'
    form = UserCreationForm()
    
    if request.method=='POST':
        form  =  UserCreationForm(request.POST)
        if form.is_valid():
            user=  form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect("home")
        else:
            messages.error(request, 'an error occured during registration')
        
        
    
    context={'form':form}
    return render(request, 'base/login_register.html',context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains =q) | 
        Q(description__icontains = q)
    )
    topics =Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    
    
    context = {'Rooms':rooms,'topics':topics, 
               "room_count":room_count, 'room_messages':room_messages}
    return render(request,'base/home.html' ,  context)
    

# @login_required(login_url="login")
def room(request,pk):
    room = Room.objects.get(id = pk)
    room_messages = room.message_set.all()
    particapants = room.participants.all()
    
    if request.method =="POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body= request.POST.get('body'),
        )
        room.participants.add(request.user)
        return redirect('room', pk = room.id)
            
    context ={'room':room,
              'room_messages':room_messages,
              'particapants': particapants}
    return render(request,'base/rooms.html',context)


def userProfile(requests, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context={'user':user, 'Rooms':rooms, 'room_messages':room_messages, 'topics':topics}
    return render(requests, 'base/profile.html',context)

  
@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method =='POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
     
        # form  = RoomForm(request.POST)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
       
        return redirect('home')
        
    context ={'form':form,'topics':topics}
    return render(request, 'base/room_form.html',context)


@login_required(login_url="login")
def updateRoom(request, pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance = room)
    topics = Topic.objects.all()
    if request.user != room.host :
        return HttpResponse("you are not authorized to update this room") 
    
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    
    context ={'form':form,'topics':topics, 'room':room}
    return render(request,'base/room_form.html',context)



@login_required(login_url="login")
def deleteRoom(request,pk):
    room = Room.objects.get(id = pk)
    context={'obj':room}
    
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',context)
        
        
@login_required(login_url="login")
def deleteMessage(request,pk):
    message = Message.objects.get(id = pk)
    
    
    if request.user != message.user:
        return HttpResponse('your are not allowed here!!')
    
    
    if request.method == "POST":
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message}) 
        
        
        
@login_required(login_url = 'login')    
def UpdateUser(request):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method =='POST':
        form =  UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
        
    
    return render(request, 'base/update_user.html', {'form':form})




def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request,'base/topics.html',{'topics':topics})



def activityPage(request):
    room_messages = Message.objects.all()
    return render(request,'base/activity.html',{'room_messages':room_messages})