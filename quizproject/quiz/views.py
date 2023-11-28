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

def quizapp(req):
    if not req.user.is_authenticated:
        return redirect('login')
    return render(req,'index.html')


def attemptQuiz(req):
    ques = db.questions.find()
    qs = list(ques)
    random_questions = random.sample(qs,5)
    return render(req,'attemptquiz.html',{'questions': random_questions})

def compareAnswers(dict1, dict2):
    score = 0
    for key in dict1:
        if dict1[key] == dict2[key]:
            score+=1
    return score

def submitquiz(req):
    if req.method == 'POST':
        submitted_answers = {}
        for key, value in req.POST.items():
            submitted_answers[key] = value
        submitted_answers.pop('csrfmiddlewaretoken')
        # for key in submitted_answers:
        #     print(key,submitted_answers[key])
        
        fetched_questions = {}
        for qid in submitted_answers.keys():
            question_data = db.questions.find_one({'qid': int(qid)})
            print(qid)
            if question_data:
                fetched_questions[qid] = question_data['correct_answer']

        # Display fetched data along with submitted answers
        for qid, correct_answer in fetched_questions.items():
            print('Question ID:', qid)
            print('Correct Answer:', correct_answer)
            print('Submitted Answer:', submitted_answers[qid])
        score = compareAnswers(submitted_answers,fetched_questions)
        return render(req,'submitquiz.html',{'answers': submitted_answers,'fetched':fetched_questions,'score':score})
