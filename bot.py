import logging
from flask import Flask, request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,Dispatcher,CallbackContext
from telegram import Bot,Update
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



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)
###############
TOKEN = "5500952298:AAH-U0dIN2Qsy-tYnuOklyDbUTzR-ZwKwvM"


app = Flask(__name__)

@app.route('/')
def index():
	return "hello !"

@app.route(f'/{TOKEN}',methods = ['GET','POST'])
def webhook():
    update = Update.de_json(request.get_json(),bot)
    dp.process_update(update)
    return "ok"

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Enter the text you want to show to the user whenever they start the bot")

def _help(update: Update, context: CallbackContext):
	update.message.reply_text("Your Message")

def describe(update: Update, context: CallbackContext):
	update.message.reply_text("this is the bot created by : A.pavan as a mini project")

def error(bot, update): # Error handler
    logger.error("Update ''%s' caused error '%s'", update, update.error)

def reply_text(update: Update, context: CallbackContext):
	intent,reply = get_reply(update.message.text, update.message.chat_id)
	if intent == "get_news":
		print(reply)
		#reply_text = "ok I will show the news with {}".format(reply)
		articels = fetch_news(reply)
		for articel in articels:
			update.message.reply_text(articel['link'])
		#bot.send_message(chat_id = update.message.chat_id,text = reply_text)
	else:
		bot.send_message(chat_id = update.message.chat_id,text = reply)


    
if __name__ == "__main__":
	bot = Bot(TOKEN)
	try:
		bot.set_webhook("https://3cc8-2409-4070-241c-e9b8-c0e6-256a-4ae3-c9e8.in.ngrok.io/"+TOKEN)
	except Exception as e:
		print(e)

	dp = Dispatcher(bot, None)
	#dp = Updater.dispatcher
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("help",_help))
	dp.add_handler(CommandHandler("describe",describe))
	dp.add_handler(MessageHandler(Filters.text ,reply_text))
	dp.add_error_handler(error)
	app.run(port= 8443)
	
    # If user types /start, call start() function
    # To provide help
    #dp.add_handler(MessageHandler(Filters.text, echo_text))     # To handle messages. We have filters to determine what type of message have we received, like, if it is text then echo_text function should be called
    #dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))       # To handle stickers
    # For handling all kind of errors

    #updater.start_polling()     # To start polling
    #logger.info("Started polling...")
    #updater.idle()      # It will wait for you to press Ctrl+C to stop polling
    
    
