from django.shortcuts import render


from django.http import HttpResponse

rooms=[
    {'id':1,'name': "Lets learn python!"},
    {'id':2,'name': "design with me"},
    {'id':3,'name': "front-end developer"},
]

def home(request):
    context = {'rooms':rooms}
    return render(request,'base/home.html' ,  context)
    


def room(request,pk):
    room = None
    for i in rooms:
        if i['id']==int(pk):
            room = i
            
    context ={'room':room}
    return render(request,'base/rooms.html',context)
    
    