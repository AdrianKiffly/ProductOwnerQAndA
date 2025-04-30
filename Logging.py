import datetime

# LOGGING ERROR, QUESTION AND RESPONSE
def log(message):
    with open("log", "a") as f:
        f.write("[" + str(datetime.datetime.now()) + "] : "+message+"\n")
