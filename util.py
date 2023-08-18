from google.cloud import dialogflow_v2 as dialogflow

from gnewsclient import gnewsclient
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "newagent-hagn-33c564c7ad5f.json"

dialogflow_session_clinet = dialogflow.SessionsClient()

projectid = "newagent-hagn"

client = gnewsclient.NewsClient()

def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_clinet.session_path(projectid, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_clinet.detect_intent(session=session, query_input=query_input)
    return response.query_result


def get_reply(query, chat_id):
    response = detect_intent_from_text(query, chat_id)

    if response.intent.display_name == 'get_news':
        return "get_news", dict(response.parameters)
    else:
        return "small_talk", response.fulfillment_text


def fetch_news(parameters):
	client.location = parameters.get('geo-country')
	client.topic = parameters.get('topics')
	client.language = parameters.get('language')
	

	return client.get_news()[:5]

