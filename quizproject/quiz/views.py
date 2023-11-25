# Create your views here.
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from pymongo import MongoClient
import random
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
    qs = []
    for q in ques:
        qs.append(q)
    print(qs[0]['question'])
    #return HttpResponse(random.sample(qs,5))
    return render(req,'attemptquiz.html',{'questions':random.sample(qs,5)})