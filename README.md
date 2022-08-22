This script counts messages in a specified Slack channel given a date range. Tested with Python 3.9.
# Weird API Limitation
conversations.history has a hidden max of 1000 for the limit parameter; if it's set to anything above that it resets to default, which is 100. 

ie if there are 107 messages and I set limit to >1000, it'll tell me there are 100 messages. If I set limit to 1000 it'll tell me there are 107.

## Boof fix:
Set limit to 1000

Split Each Day into
0000-1200 (1000 max msgs for this period)
1200-2359 (1000 max msgs for this period)

MUCH slower as we're sending a bunch of API calls instead of 1, but whatever. Works now.


# Setup
* `pip install -r requirements.txt` to get slack-sdk
* Go to api.slack.com/apps, Create New App > From Scratch > Name it anything.
* OAuth & Permissions tab > User Token Scopes > Add an OAuth Scope

Add the following scopes:
* channels:history
* channels:read
* groups:history
* groups:read
* im:history
* im:read
* mpim:history
* mpim:read

Scroll up and hit "Install to Workspace" > Hit "Allow"

Copy the User OAuth Token, paste into Line 12 double quotes
Specify channel name on line 13

# Usage
`python3 slackStats.py 01-01-2022` for number of messages in channel on 01-01-2021

`python3 slackStats.py 01-01-2022 01-08-2022` for number of messages in channel between 01-01-2022 and 01-08-2022 (inclusive)

`python3 slackStatscsv.py` outputs `dailyTix.csv`, counts tickets for every day specified in range in script