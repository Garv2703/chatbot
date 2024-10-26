from pprint import pprint
from flask import Flask, render_template, request, jsonify, session
import google.generativeai as genai, os, markdown2

app = Flask(__name__)
app.secret_key = 'flask-insecure-ot%!h9epy)g9scdb^$)ymmt&#@ca=pyjg+7-p_yh89di6g0^c5'

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
    resp = markdown2.markdown(resp)

    history.append({'role': 'user', 'parts': prompt})
    history.append({'role': 'model', 'parts': resp})
    
    return resp

@app.route('/')
def index():
    return render_template('index.html', chat_history=history)

@app.route('/get-response', methods=['POST'])
def get_response():
    user_input = request.form['user_input'].strip()
    response = get_gemini_response(user_input)
    return jsonify({'chatbot_response': response, 'user_input': user_input})

@app.route('/clear-chat')
def clear_chat():
    global history
    history.clear()
    history=[
        {'role':'user', 'parts':'Hello'},
        {'role':'model', 'parts':"Great to meet you. What would you like to know?"}
    ]
    btn_var = request.args.get('btn')
    if btn_var == 'new':
        global chat
        chat = model.start_chat(history=history)
        
    return jsonify({'message': 'success'})

if app.name == '__main__':
    app.run(debug=True)