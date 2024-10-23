from flask import Flask, render_template, request, jsonify
import google.generativeai as genai, os, markdown2

app = Flask(__name__)

API_KEY = 'AIzaSyB2kJq_QfzrLx3qyc_50o1QtzkseukiXXk'
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
history=[
    {'role':'user', 'parts':'Hello'},
    {'role':'model', 'parts':"Great to meet you. What would you like to know?"}
]
chat = model.start_chat(history=history)

def get_gemini_response(prompt):
    global chat
    response = chat.send_message(prompt)
    resp = response.text

    history.append({'role': 'user', 'parts': prompt})
    history.append({'role': 'model', 'parts': resp})

    resp = markdown2.markdown(resp)
    return resp

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-response', methods=['POST'])
def get_response():
    user_input = request.form['user_input'].strip()
    response = get_gemini_response(user_input)
    return jsonify({'chatbot_response': response, 'user_input': user_input})

if app.name == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai, os, markdown2

app = Flask(__name__)

API_KEY = 'AIzaSyB2kJq_QfzrLx3qyc_50o1QtzkseukiXXk'
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
history=[
    {'role':'user', 'parts':'Hello'},
    {'role':'model', 'parts':"Great to meet you. What would you like to know?"}
]
chat = model.start_chat(history=history)

def get_gemini_response(prompt):
    global chat
    response = chat.send_message(prompt)
    resp = response.text

    history.append({'role': 'user', 'parts': prompt})
    history.append({'role': 'model', 'parts': resp})

    resp = markdown2.markdown(resp)
    return resp

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-response', methods=['POST'])
def get_response():
    user_input = request.form['user_input'].strip()
    response = get_gemini_response(user_input)
    return jsonify({'chatbot_response': response, 'user_input': user_input})

if app.name == '__main__':
    app.run(debug=True)