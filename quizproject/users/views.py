from django.shortcuts import render,redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from django.http import HttpResponse


# Create your views here.
def register(req):
    if req.method == 'POST':
        form = UserRegistrationForm(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            return HttpResponse("Saved")
    else:
        form = UserRegistrationForm()
    return render(req,'signup.html',{'form':form})