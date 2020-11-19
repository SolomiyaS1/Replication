from flask import Flask, jsonify, request
from flask import abort
from jsonrpcclient.clients.http_client import HTTPClient
import json
from app import app

#app = Flask(__name__)
secondary_url = ['http://localhost:80/messages', 'http://localhost:8080/messages']

messages = [
    {
        'id': 1,
        'text': 'test message'
    }
]


@app.route('/')
def index():
    return 'Master node is running...'


@app.route('/messages', methods=['GET'])
def get_tasks():
    return jsonify({'messages': messages})

@app.route('/messages', methods=['POST'])
def create_task():
    if not request.json or not 'text' in request.json:
        abort(400)
    message_id = []
    print(request.json['text'])
    message = {
        'jsonrpc': '2.0',
        'method': 'save_message',
        'params': {'text': request.json['text']},
        'id': messages[-1]['id'] + 1
    }
    messages.append(message)
    for i in range(0, len(secondary_url)):
        client = HTTPClient(secondary_url[i])
        response = client.send(json.dumps(message))
        message_id.append(response.data.id)
    return jsonify({'MessageId': message_id}), 201


'''def setup():
    app.run(debug=True, port=5000)'''
