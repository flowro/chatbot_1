from flask import Flask, request, render_template, jsonify, make_response
from nltk import word_tokenize
#from custom_module import function1, function2  # custom python module
import logging
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index_delay.html")

def process_text(text):
    tokens = word_tokenize(text)
    # Very basic intent processing
    if "greeting" in tokens:
        return "greeting"
    if "help" in tokens:
        return "help"
    else:
        return "unknown"
    
@app.route("/ask", methods=['POST','GET'])
def ask():
    question = request.json.get('question')
    print(question)
    intent = process_text(question)
    answer = ""

    # log the question, intent and answer
    log_data = {
        'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'question': question,
        'intent': intent,
        'answer': answer,
    }
    logging.info(str(log_data))
    
    # Depending on the intent, call different functions
    if intent == "greeting":
        response = jsonify(answer="this is a test for greeting")  # from your custom python module
    elif intent == "help":
        response = jsonify(answer="this is a test for help")  # from your custom python module
    else:
        response = jsonify(answer="I'm not sure how to respond to that.")
    
    print(response)

    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response = make_response(response)

    #response = make_response(jsonify(answer="This is a test response"))
    #response.headers['Content-Type'] = 'application/json; charset=utf-8'

    return response

if __name__ == '__main__':
    app.run(debug=True)