from flask import Flask, render_template, request, jsonify
import google.generativeai as genai, os, markdown2
from google.generativeai.types import HarmBlockThreshold, HarmCategory

app = Flask(__name__)
app.secret_key = 'flask-insecure-ot%!h9epy)g9scdb^$)ymmt&#@ca=pyjg+7-p_yh89di6g0^c5'

API_KEY = os.environ.get('API_KEY')

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction='You are an animal in the Jungle Parliament, presiding over discussions and offering wise council as a parliament member. Respond in the voice of an elder animal, offering advice or answers with wisdom, charm, and authority as though in a council meeting among animals.',
)

history=[
    {'role': 'user', 'parts': 'Hello Animals! Jungle Parliament!'},
    {'role': 'model', 'parts': "Greetings, animal! I am Owl, wise overseer of the Jungle Parliament. What wisdom do you seek from the council today?"}
]
chat = model.start_chat(history=history)

def get_gemini_response(prompt):
    global chat
    response = chat.send_message(
        prompt,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            # HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        }
    )
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