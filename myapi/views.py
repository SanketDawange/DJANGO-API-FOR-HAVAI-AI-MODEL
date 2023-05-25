from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from .models import UserDetail, UserFile, Category, Scheme, Hospital

from . import NeuralNetwork
from . import Brain
import random
import json
import torch
import random

# ---------------
# -------------------------------------------------------------------------------------
device = torch.device('cuda' if torch .cuda.is_available() else 'cpu')
with open("media/intents.json","r") as json_data:
    intents = json.load(json_data)

FILE = "media/TrainData.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = Brain.NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

# ----------------------------------------------------------------------------------------




# Create your views here.
def home(request):
    return render(request,"home.html")


def getResponse(request, user_message):
    user_message = str(user_message).lower()
    sentence = NeuralNetwork.tokenize(user_message)
    X = NeuralNetwork.bag_of_words(sentence,all_words)
    X = X.reshape(1,X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _ , predicted = torch.max(output,dim=1)

    tag = tags[predicted.item()]
    probs = torch.softmax(output,dim=1)
    prob = probs[0][predicted.item()]

    reply =""
    if prob.item() > 0.75:
        for intent in intents['intents']:

            if tag == intent["tag"]:
                reply = random.choice(intent["responses"])

    
    # ----------------------------------------------------------------
    NOT_UNDERSTOOD_RESPONSES = [
        "Sorry my bad, I could not understant",
        "I'm sorry, I couldn't find any data related to that. Can you please try a different query or provide more context?",
        "I'm sorry, I'm not able to find a dataset associated with your request. Can you try rephrasing or providing more details?",
        "My apologies, I couldn't retrieve the requested data. Would you like to try again with a different query?",
        "Sorry, I couldn't understand your request and couldn't find any related data. Can you please try a different query or provide more information?"
    ]
    if reply == "":
        reply = NOT_UNDERSTOOD_RESPONSES[random.randint(0, len(NOT_UNDERSTOOD_RESPONSES)-1)]
    model_response = {'response': reply}
    return JsonResponse(model_response)


def makeAppointment(request, user_message):
    user_message = user_message.lower()
    if user_message.count("book") >=1 or user_message.count("appointment") >=1:
        user_message = "Select near by hospitals to book an appointment like Shantanu Hospital, rahul Hospital, sanket Hospital or shreyash hospital"
    elif user_message.count("shantanu") >=1 :
        user_message = "00"
    elif user_message.count("rahul") >=1 :
        user_message = "01"
    elif user_message.count("sanket") >=1 :
        user_message = "02"
    elif user_message.count("shreyash") >=1 or user_message.count("shreyas") >=1 :
        user_message = "03"
    else:
        user_message = "Please choose a hospital first."
    

    model_response = {'response': user_message}
    return JsonResponse(model_response)



def signUp(request, username, password):
    if username != None and password != None:
        if User.objects.filter(username = username).exists():
            return JsonResponse({"status":"username taken"})
            # if new user is registering 
        myuser=User.objects.create_user(username,username+"@techvedh.com",password)
        myuser.save()
        print("User registered", username)
        return JsonResponse({"status":"success"})
    return JsonResponse({"status":"error"})

def loginUser(request, username, password):
    if username != None and password != None:
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            print("User logged in", username)
            return JsonResponse({"status":"success"})
        else:
            return JsonResponse({"status":"invalid"})
        
    return JsonResponse({"status":"error"})

def getUserDetails(request, username):
    user = User.objects.filter(username=username)
    if len(user):
        user_detail = UserDetail.objects.filter(user = user[0])
        context = {
            "user_detail" : user_detail
        }
        return render(request,"user_details.html", context)
    return HttpResponse("User details not found")

def getUserDocs(request, username, key):
    user_detail = UserDetail.objects.filter(key = key)
    if len(user_detail):
        user = User.objects.get(username=username)
        user_files = UserFile.objects.filter(user = user)
        context = {
            "user" : user,
            "user_files" : user_files
        }
        return render(request,"docs.html", context)
    
    user = User.objects.filter(username=username)
    if len(user):
        user_detail = UserDetail.objects.filter(user = user[0])
        context = {
            "user_detail" : user_detail,
            "error_message":"Invalid secrete key"
        }
        return render(request,"user_details.html", context)
    return HttpResponse("User details not found")
    

def doctor_signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if User.objects.filter(username = username).exists():
            return render(request, "doctor_signup.html",{"error":"Username already taken! "})
        if pass1 != pass2:
            return render(request, "doctor_signup.html",{"error":"Password do not match"})

        myuser=User.objects.create_user(username,email,pass1)
        myuser.save()

        return redirect("doctor_dashboard")
    
    return render(request, "doctor_signup.html",)

def doctor_signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        user=authenticate(username=username,password=pass1)
        if user is not None:
            login(request,user)
            print("User logged in", username)
            return redirect("doctor_dashboard")
        else:
            return render(request, "doctor_signin.html",{"error":"Incorrect username or password"})
        
    return render(request, "doctor_signin.html")

def doctor_dashboard(request):
    if request.user.is_authenticated == False:
        return redirect("login")
    return render(request, "doctor_dashboard.html")

def doctor_logout(request):
    if request.user.is_authenticated == False:
        return redirect("login")
    logout(request)
    return redirect("doctor_signin")

def getCategories(request):
    array_1 = []
    for obj in Category.objects.all():
        array_1.append(obj.name)
    return JsonResponse({"cats":array_1})
    
def getSchemes(request, category):
    categ=Category.objects.get(name=category)
    schemes= Scheme.objects.filter(category=categ)
    array_1 = []
    for obj in schemes:
        array_1.append(obj.name)
    return JsonResponse({"schemes":array_1})

def getHospitals(request, scheme):
    sch=Scheme.objects.get(name=scheme)
    hospi= Hospital.objects.filter(scheme=sch)
    array_1 = []
    for obj in hospi:
        array_1.append(obj.name)
    return JsonResponse({"hospitals":array_1})
