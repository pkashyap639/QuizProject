from django.shortcuts import render,redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from django.http import HttpResponse


# Create your views here.
def register(req):
    if req.user.is_authenticated:
        return redirect('/quizapp/')
    if req.method == 'POST':
        form = UserRegistrationForm(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(req,'signup.html',{'form':form})

def login(req):
    if req.user.is_authenticated:
        return redirect('/quizapp/')

def logout(req):
    if not req.user.is_authenticated:
        return redirect('//')
    return redirect('login')