from flask import Flask, jsonify, request
from flask import abort
from jsonrpcclient.clients.http_client import HTTPClient
import json
from app import app
from threading import Thread
import queue

secondary_url = ['http://secondary:8000/messages', 'http://anothersecondary:8080/messages']

#secondary_url = ['http://localhost:8000/messages', 'http://localhost:8080/messages']

messages = []

write_concern = 2


@app.route('/')
def index():
    return 'Master node is running...'


@app.route('/messages', methods=['GET'])
def get_tasks():
    return jsonify({'messages': messages})

@app.route('/configs', methods=['GET'])
def get_configs():
    return jsonify({'write_concern': write_concern})

@app.route('/configs', methods=['POST'])
def update_configs():
    if not request.json or not 'write_concern' in request.json:
        abort(400)
    global write_concern
    print(request.json['write_concern'])
    write_concern = int(request.json['write_concern'])
    return jsonify({'write_concern': write_concern}), 201


@app.route('/messages', methods=['POST'])
def create_task():
    if not request.json or not 'text' in request.json:
        abort(400)

    message_id = []
    text = request.json['text']
    if len(messages) == 0:
        id = 1
    else:
        id = len(messages) + 1
    message = {
        'jsonrpc': '2.0',
        'method': 'save_message',
        'params': {'text': text},
        'id': id
    }
    messages.append(text)
    message_id.append(id)
    q = queue.Queue()
    threads = [Thread(target=message_sender, args=(secondary_url[i], message, message_id, q)) for i in
               range(0, len(secondary_url))]

    if write_concern == 1:
        for thread in threads:
            thread.start()
        print(message_id)
        return jsonify({'MessageId': message_id}), 201

    if write_concern == 3:
        print(write_concern)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return jsonify({'MessageId': message_id}), 201

    if write_concern == 2:
        for thread in threads:
            thread.start()
        q.get()
        return jsonify({'MessageId': message_id}), 201


def message_sender(secondary_url, message, message_id, result_queue):
    client = HTTPClient(secondary_url)
    response = client.send(json.dumps(message))
    message_id.append(response.data.id)
    result_queue.put(response.data.id)
