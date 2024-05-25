from django.shortcuts import render


from django.http import HttpResponse


def home(requests):
    return HttpResponse("home page")


def room(request):
    return HttpResponse("<title>Room page</title>Room page")
    