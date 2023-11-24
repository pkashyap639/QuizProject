# Create your views here.
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse


# Create your views here.
def quizapp(req):
    return HttpResponse("QUIZAPP",req)