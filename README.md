This script counts messages in a specified Slack channel given a date range. Tested with Python 3.9.

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



# NOTE
If there are over 1000 tickets from 0000-1200 or 1259-2359 it will cap for that period


## Weird API Limitation
conversations.history has a hidden max of 1000 for the limit parameter; if it's set to anything above that it resets to default, which is 100. 

ie if there are 107 messages and I set limit to >1000, it'll tell me there are 100 messages. If I set limit to 1000 it'll tell me there are 107.

## Boof fix:
Set limit to 1000

Split Each Day into
0000-1200 (1000 max msgs for this period)
1200-2359 (1000 max msgs for this period)

MUCH slower as we're sending a bunch of API calls instead of 1, but whatever. Works now.


## Potential Improvements
The code can definitely be cleaned up in general.

Best thing would be not splitting the days unless a message cap is detected and splitting it even further than two if necessary (fixing the 1000 cap on 12-hr intervals). Eliminating the 0000-1200 & 1200-2359 split where it's unnecessary would p much double the speed (but who cares honestly, this is good enough).