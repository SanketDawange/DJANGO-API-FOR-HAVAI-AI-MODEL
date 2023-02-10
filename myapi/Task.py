import datetime

     # Non Input functions 
def Time():
    time = datetime.datetime.now().strftime("%H,%M")
    return (time)

def Date():
    date = datetime.date.today()
    return (date)

def Day():
    day = datetime.datetime.now().strftime("%A")
    return (day)


    # Input Functions 
def NonInputExecution(query):

    query = str(query)
    if "time" in query:
        Time()

    elif "date" in query:
        Date()

    elif "day" in query:
        Day()


def InputExecution(tag,query):

    if "wikipedia" in tag:       
        name = str(query).replace("who is","").replace("about","").replace("what is","").replace("Tell me about","").replace("wikipedia ","")
        import wikipedia
        result = wikipedia.summary(name)
        return (result)

    elif "google" in tag:
        query = str(query).replace("Google search","")
        query = query.replace("search","")
        import pywhatkit
        pywhatkit.search(query)


