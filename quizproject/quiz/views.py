# Create your views here.
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from pymongo import MongoClient
import random
import json

# Mongo Client
client = MongoClient('mongodb+srv://pkashyap148:*Password123@quizcluster.dzltjq0.mongodb.net/?authMechanism=DEFAULT')
db = client['quizproject']
# Create your views here.
def quizapp(req):
    if not req.user.is_authenticated:
        return redirect('login')
    return render(req,'index.html')

# def getQuestions():
#     ques = quizproject.questions.find()
#     return ques


def attemptQuiz(req):
    ques = db.questions.find()
    qs = list(ques)
    random_questions = random.sample(qs,5)
    return render(req,'attemptquiz.html',{'questions': random_questions})

def submitquiz(req):
    if req.method == 'POST':
        submitted_answers = {}
        for key, value in req.POST.items():
            submitted_answers[key] = value
        for key in submitted_answers:
            print(key,submitted_answers[key])
        return render(req,'submitquiz.html',{'answers': submitted_answers})
