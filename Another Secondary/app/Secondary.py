import random as rand

from flask import jsonify, request, Response
from jsonrpcserver import method, dispatch
from app import app
import time

messages = {}
buffer = {}

@method
def save_message(text, messageId):
    #messages.append(text)
    if messages:
        masseges_max_key = max(messages)
    else:
        masseges_max_key = 0

    if messageId - masseges_max_key > 1:
        buffer[messageId] = text
    elif messageId not in messages:
        messages[messageId] = text

    if messages:
        masseges_max_key = max(messages)
    else:
        masseges_max_key = 0
    if buffer:
        buffer_min_key = min(buffer)
    else:
        buffer_min_key = 0

        while buffer_min_key - masseges_max_key == 1:
            messages[buffer_min_key] = buffer[buffer_min_key]
            del buffer[buffer_min_key]
            buffer_min_key = min(buffer)

    print(text)
    return messageId


@app.route('/')
def index():
    return 'Secondary node is running...'


@app.route('/messages', methods=['GET'])
def get_tasks():
    return jsonify({'messages': messages})

@app.route('/buffer', methods=['GET'])
def get_buffer():
    return jsonify({'buffer': buffer})


@app.route('/messages', methods=['POST'])
def create_task():
    req = request.get_data().decode()
    rnd = rand.randint(1, 20)
    print(rnd)
    time.sleep(rnd)
    #time.sleep(10)
    response = dispatch(req)
    return Response(str(response), response.http_status, mimetype="application/json")
