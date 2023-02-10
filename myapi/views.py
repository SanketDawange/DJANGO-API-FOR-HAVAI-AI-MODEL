from django.http import HttpResponse,JsonResponse
from . import NeuralNetwork
from . import Brain
import random
import json
import torch

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


    model_response = {'response': reply}
    return JsonResponse(model_response)
