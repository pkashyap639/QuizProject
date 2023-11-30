# Create your views here.
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from pymongo import MongoClient
import random
import json
from datetime import datetime

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

def getScoreMsg(score):
    msg = ""
    if score == 5:
        msg = f'Score: {score}/5, You are a Genius !'
    if score == 4:
        msg = f'Score: {score}/5, Excellent Work!'
    if score == 3:
        msg = f'Score: {score}/5, Good Job !'
    if score == 1 or score ==2 or score ==0:
        msg = f'Score: {score}/5, Please Try Again!'

    return msg

def storeQuizData(score,username,useremail):
    now = datetime.now()
    stringTime = now.strftime("%d/%m/%Y %H:%M:%S")
    checkExistence = db.quiz_data.find_one({"useremail":useremail})
    if checkExistence is None:
        quizData = {
            "useremail": useremail,
            "username": username,
            "quizes": [{
                "score": score,
                "time" : stringTime
            }]
        }
        db.quiz_data.insert_one(quizData)
        print("Data INserted For the First Time")
    else:
        query = {"useremail": useremail}
        update_data = {"$push": {"quizes": {"score": score, "time": stringTime}}}
        db.quiz_data.update_one(query, update_data)
        print("Data Updated")
    

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
        msg = getScoreMsg(score)
        storeQuizData(score,req.user.username, req.user.email)
        return render(req,'submitquiz.html',{'answers': submitted_answers,'fetched':fetched_questions,'score':score,'msg':msg})
