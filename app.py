from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

API_URL = "http://127.0.0.1:1337/v1"
API_KEY = "your_api_key_here"  # Replace with your actual API key if required


def generate_response(prompt):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    data = {
        'model': 'aya-23-8b',  # أو اسم المودل الخاص بك
        'messages': [{'role': 'user', 'content': prompt}]
    }
    response = requests.post(f"{API_URL}/chat/completions", headers=headers, json=data)
    return response


@app.route('/')
def home():
    return render_template('index.html', model_name='aya-23-8b')  # أو اسم المودل الخاص بك


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = generate_response(user_input)

    if response.status_code == 200:
        response_json = response.json()
        if 'choices' in response_json and response_json['choices']:
            chatbot_message = response_json['choices'][0]['message']['content']
            return jsonify({'message': chatbot_message})
        else:
            return jsonify(
                {'message': 'Sorry, there was an error processing your request. No choices found in response.'})
    else:
        return jsonify(
            {'message': f'Sorry, there was an error processing your request. Status code: {response.status_code}'})


if __name__ == "__main__":
    app.run(debug=True)
