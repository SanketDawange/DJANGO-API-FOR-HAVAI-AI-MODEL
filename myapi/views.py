from django.http import HttpResponse,JsonResponse
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
    return HttpResponse("API")


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
    if user_message.count("book") >=1 or user_message.count("appointment") >=1:
        user_message = "With whome you want to make an appointment"
        user_message = "Select near by hospitals to book an appointment like Hinjawadi Hospital, Shree Hospital, Ankur Hospital or specify"
    if user_message.count("Hinjawadi") >=1:
        user_message = "Doctor shyam mehta(Dentist) and piyush gupta(Orthopedic) are availabe at Hinjawadi Hospital, with whome you wanna make appointment"
    if user_message.count("shyam") >=1 or user_message.count("mehta") >=1:
        user_message = "Your appointment has been sent to shyam mehta"
    if user_message.count("piyush") >=1 or user_message.count("gupta") >=1:
        user_message = "Your appointment has been sent to piyush gupta"
    if user_message.count("Shree"):
        user_message = "At this moment Shree hospital is not accepting bookings"
    if user_message.count("Ankur"):
        user_message = "Your appointment has been sent to Ankur Hospital you will recieve more information about your appointment shortly.."
    else: user_message = "Sorry your requested facilty isn't available."

    model_response = {'response': user_message}
    return JsonResponse(model_response)