#coding=utf-8
from __future__ import print_function
import random, math

# ===================================

# This is what the skill is called.
SKILL_NAME = "" # Example: "Beatbox"

# This is what the user says to open the skill. Aka, "Alexa, open INVOCATION_NAME"
INVOCATION_NAME = "" # Example: "beat boxer"

# This is the title of the box that pops up in the Alexa app, commonly known as a "card".
CARD_TITLE = "" # Example: "Beat Boxer"

# This is what is said when Alexa is asked for help. Aka, "Alexa, ask INVOCATION_NAME for help"
OPEN_TEXT = "Welcome to the {} skill. To start this skill, simply ask\n'Alexa, start {}.'".format(SKILL_NAME, INVOCATION_NAME) # Change this to something more fitting!

# This is what is said when Alexa is opened without any intents. Aka, "Alexa, open INVOCATION_NAME" or "Alexa, start INVOCATION_NAME".
HELP_TEXT = OPEN_TEXT

# This is what is said when Alexa has been canceled or stopped. I'd advise you keep this empty.
GOODBYE_TEXT = ""

# ===================================

# The intent database:
# This is what forwards the intents (the different functions) to different functions.

from intents import *

# If you program the corresponding functions for the intents in the "intents.py" file and link them in here, then it should handle it for you.
INTENT_DATABASE = {
    "example": example # When the user triggers the intent "example", the function example() is called from the intents.py file.
}

# ===================================

# This part is used to parse strings into something the Amazon Alexa can understand.
# You don't need to change any of this.

def speech(output):
    return {
        "type": "SSML",
        "ssml": "<speak>" + output + "</speak>"
    }

def reprompt(output):
    return {
        "type": "SSML",
        "ssml": "<speak>" + output + "</speak>"
    }

def card(title, content, image = ["", ""]):
    if image == ["", ""]:
        return {
            "type": "Simple",
            "title": title,
            "content": content
        }

    else:
        return {
            "type": "Standard",
            "title": title,
            "text": content,
            "image": {
                "smallImageUrl": image[0],
                "largeImageUrl": image[1]
            }
        }

def response(speech_response, reprompt_response, card_response, should_end = True, session_attributes = {}, version = "1.0"):
    return {
        "version": version,
        "sessionAttributes": session_attributes,
        "response": {
            "outputSpeech": speech_response,
            "card": card_response,
            "reprompt": {
                "outputSpeech": reprompt_response
            },
            "shouldEndSession": should_end
        }
    }

def text(string):
    # This function takes a string, or an array 3 long, and turns it into something Alexa can understand.
    # The format for the array is like so: [said text, card title (what's shown in the Alexa app), card text.]
    if type(string) == list:
        if len(string) == 3:
            # This means it is indeed an array 3 long.
            return response(speech(string[0]), reprompt(""), card(string[1], string[2]), should_end = True)

    else:
        return response(speech(string), reprompt(""), card(SKILL_NAME, string), should_end = True)

# ===================================

# These are the functions that handle other things the user can do to the skill that aren't intents.

def stop(intent, session):
    # This just means that the Alexa skill will end when the function is called.
    return response(speech(GOODBYE_TEXT), reprompt(""), card("", ""), should_end = True)

def aid(intent, session):
    # If the user asks for help, this function is called.
    print("User has asked for help.")
    return response(speech(HELP_TEXT), reprompt(""), card(SKILL_NAME, HELP_TEXT), should_end = False)

def on_launch(launch_request, session):
    # User launched the app without specifying what they want to do. For example, "Alexa, open <SKILL NAME>" or "Alexa, start <SKILL NAME>"
    print("User launched the app without specifying what they want to do.")
    return response(speech(OPEN_TEXT), reprompt(""), card(SKILL_NAME, OPEN_TEXT), should_end = False)

def on_session_started(session_started_request, session):
    print("Session started.")
    return

def on_session_ended(session_ended_request, session):
    print("Session ended.")

# ===================================


def on_intent(intent_request, session):
    # This handles what happens when an intent is triggered. This is taken care of automatically, so you shouldn't need to change anything.
    # This uses the data from the INTENT_DATABASE above.

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    print("User just issued intent: {}".format(intent_name))

    for intent in INTENT_DATABASE.keys():
        if intent_name == intent:
            return text(INTENT_DATABASE[intent]())

    if intent_name == "CancelIntent" or intent_name == "Cancel" or intent_name == "AMAZON.CancelIntent" or intent_name == "StopIntent" or intent_name == "Stop" or intent_name == "AMAZON.StopIntent":
        return stop(intent, session)

    elif intent_name == "HelpIntent" or intent_name == "Help" or intent_name == "AMAZON.HelpIntent":
        return aid(intent, session)


def lambda_handler(event, context):
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']}, event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])

    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])

    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
