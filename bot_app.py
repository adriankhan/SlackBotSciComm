import os
from slackeventsapi import SlackEventAdapter
from slack import WebClient
from flask import Flask, jsonify, Response

app = Flask(__name__)

SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events", app)
slack_client = WebClient(SLACK_BOT_TOKEN, timeout=30)

# Message block generator
def msg_block():

    '''Implemented later'''

    # Not yet implemented
    pass


# Team Join Event
# Adapter listens for event notifications of a new user joining the Slack team.
# This decorator assigns a function to the 'team_join' event, triggering the welcome message callback.

@slack_events_adapter.on('team_join')
def user_joined(event_data):
    
    '''Accepts the event data payload from the Slack Events API.
    Accesses the Slack Client API to send a direct welcome message to a new user joining the team.'''

    pass

# Join test channel response
# Adapter listens for user joining a test channel

@slack_events_adapter.on('member_joined_channel')
def channel_welcome(event_data):

    '''Moniter channel joining and send a relevant welcome message.'''

    print(event_data)
    print('x')
    event = event_data.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    slack_client.chat_postMessage(channel=channel_id,text='I see you.')

    pass

@slack_events_adapter.on('message')
def reg_message(event_data):

    print(event_data)
    print('y')
    event = event_data.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')

    response = slack_client.conversations_open(users = user_id)
    channel = response['channel']['id']
    slack_client.chat_postMessage(channel=channel,text="This is a test message.")

    
# Catch error events with the API listener

@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))


    pass

# Decorator and function to route slash commands outside of the events API adapter.

@app.route('/slash', methods=['POST'])
def slash():
    print("This worked.")

    payload = {'text': 'SciComm Bot slash command received.'}
    
    return jsonify(payload), 200

# Only run the server if this file is being run as the main file, not as a module.

if __name__ == "__main__":

    # Utilize the adapter's built-in Flask instance
    # Handles the challenge URL validation steps automatically

    # Heroku dynamically sets $PORT, which can be called via an environmental variable
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)
    # slack_events_adapter.start(host='0.0.0.0', port=port)
