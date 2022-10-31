import logging
import csv
import argparse
import sys
from datetime import datetime
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
userToken="" # BOT oath token
channel = "cus-smallchat"
filename='smallchat.csv'
fields = ['Date', 'Ticket Count']
rows = []
startDateTS = datetime.strptime("10-20-2022", "%m-%d-%Y").timestamp()
endDateTS = datetime.strptime("10-26-2022", "%m-%d-%Y").timestamp()
endDateTS+=86400

###################################################################
# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=userToken)
logger = logging.getLogger(__name__)
# logging.basicConfig(level="DEBUG")
conversations_store = {}
totalTotalMessages=0

def fetch_conversations():
    try:
        # Call the conversations.list method using the WebClient
        result = client.conversations_list(types="private_channel") #types="public_channel,private_channel" did NOT work
        save_conversations(result["channels"])

    except SlackApiError as e:
        logger.error("Error fetching conversations: {}".format(e))


# Put conversations into the JavaScript object
def save_conversations(conversations):
    conversation_id = ""
    for conversation in conversations:
        # Key conversation info on its unique ID
        conversation_id = conversation["id"]

        # Store the entire conversation object
        conversations_store[conversation_id] = conversation


channel_id = ""
fetch_conversations()

for key in conversations_store:
    if(conversations_store[key]["name"]==channel):
        channel_id =conversations_store[key]["id"]
        # print(channel_id)
###########################################################
def getTotalMsgs(startDateTS, endDateTS):
    conversation_history = []
    totalMessages = 0
    global totalTotalMessages
    try:
        result = client.conversations_history(channel=channel_id, limit=1000, latest=str(endDateTS+1), oldest=str(startDateTS-1), inclusive=True)

        conversation_history = result["messages"]
        # print(conversation_history)
        # Print results
        logger.info("{} messages found in {}".format(len(conversation_history), id))
        # print((len(conversation_history)))
    except SlackApiError as e:
        logger.error("Error creating conversation: {}".format(e))



    for msg in conversation_history:
        ticketTime = float(msg["ts"])
        if ticketTime >= startDateTS and ticketTime<endDateTS:
            if "subtype" in msg.keys() and msg["subtype"] == "channel_join":
                totalMessages+=0
            elif "subtype" in msg.keys() and msg["subtype"] == "bot_message" and msg["username"]=="Smallchat":
                totalMessages+=1
            else:
                totalMessages+=0

    #TODO add to rows current date and messages from date
    ts = datetime.fromtimestamp(startDateTS)
    rows.append([ts.strftime("%m-%d-%Y"),totalMessages])
    # print("Total Messages: ",totalMessages)



while ((endDateTS-startDateTS)>=86400): # if range geq 12 hours
    getTotalMsgs(startDateTS,startDateTS+86400)
    startDateTS=startDateTS+86400
# print("Total Messages: ",totalTotalMessages)

# daily ticket count from july 1 thru yesterday (put in csv, seems easiest)

# writing to csv file
with open(filename, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    # writing the data rows
    csvwriter.writerows(rows)