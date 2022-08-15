""" Please run command like so:
python3 slackStats.py 01-01-2021 OR python3 slackStats.py 01-01-2021 01-08-2021
The second date is inclusive (messages from 01-08-2021 will be included in the previous command)
"""
import logging
import argparse
import sys
from datetime import datetime
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

######################################################################################
## Parse input dates
startDateTS = 0
endDateTS = 0
exampleString = "Please run command like so: python3 slackStats.py 01-01-2021 OR python3 slackStats.py 01-01-2021 01-08-2021"
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('startDate', nargs='?')
parser.add_argument('endDate', nargs='?')
args = parser.parse_args()
if args.startDate == None:
    sys.exit("Invalid first date! "+exampleString)
else:
    try:
        startDateTS = datetime.strptime(args.startDate, "%m-%d-%Y").timestamp()
    except:
        sys.exit("Invalid first date! "+exampleString)
if args.endDate == None:
    endDateTS = startDateTS+86400
else:
    try:
        endDateTS = datetime.strptime(args.endDate, "%m-%d-%Y").timestamp()+86400
    except:
        sys.exit("Invalid second date! "+exampleString)

###################################################################

# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token="xoxp-3920276120773-3925689939060-3935876797027-590a5c0bc4413e2bcd12a7b5874c92e6")
logger = logging.getLogger(__name__)
# logging.basicConfig(level="DEBUG")
conversations_store = {}
totalMessages=0

def fetch_conversations():
    try:
        # Call the conversations.list method using the WebClient
        result = client.conversations_list()
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

channel = "general"
channel_id = ""
fetch_conversations()
for key in conversations_store:
    if(conversations_store[key]["name"]==channel):
        channel_id =conversations_store[key]["id"]
        # print(channel_id)
###########################################################

# Store conversation history
conversation_history = []
try:
    result = client.conversations_history(channel=channel_id, limit=1000, latest=str(endDateTS+1), oldest=str(startDateTS-1), inclusive=True)

    conversation_history = result["messages"]

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
        else:
            totalMessages+=1


print("Total Messages: ",totalMessages)