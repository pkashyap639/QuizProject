# Create your views here.
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse


# Create your views here.
def quizapp(req):
    if not req.user.is_authenticated:
        return redirect('login')
    return render(req,'index.html')