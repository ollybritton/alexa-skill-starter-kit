#coding=utf-8
from __future__ import print_function
import random, math

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

def get_random():
    with open("phrases.txt", "r") as f:
        return random.choice(f.readlines())

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

def inspire(intent, session):
    return response(speech("Hey"), reprompt("Hey"), card("Hey", "Hey"))

def on_session_started(session_started_request, session):
    print("Session started.")
    return


def on_launch(launch_request, session):
    return


def on_session_ended(session_ended_request, session):
    print("Session ended.")


def on_intent(intent_request, session):
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    print("User just issued intent: {}".format(intent_name))

    if intent_name == "Inspire":
        return inspire(intent, session)


def request(event, context):
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']}, event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])

    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])

    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
