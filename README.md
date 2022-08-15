Limitation: only 1000 messages at a time can be read

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

Copy the User OAuth Token, paste into Line 41 double quotes

Specify channel name on line 67

# Usage
`python3 slackStats.py 01-01-2022` for number of messages in channel on 01-01-2021

`python3 slackStats.py 01-01-2022 01-08-2022` for number of messages in channel between 01-01-2022 and 01-08-2022 (inclusive)