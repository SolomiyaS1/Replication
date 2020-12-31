from flask import jsonify, request, Response
from jsonrpcserver import method, dispatch
from app import app

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

    if buffer:
        buffer_min_key = min(buffer)
    else:
        buffer_min_key = 0

        while buffer_min_key - masseges_max_key == 1:
            messages[buffer_min_key] = buffer[buffer_min_key]
            del buffer[buffer_min_key]

    print(text)
    return messageId


@app.route('/')
def index():
    return "Secondary node is running..."


@app.route('/messages', methods=['GET'])
def get_tasks():
    return jsonify({'messages': messages})


@app.route('/messages', methods=['POST'])
def create_task():
    req = request.get_data().decode()
    response = dispatch(req)
    print(str(response), response.http_status)
    return Response(str(response), response.http_status, mimetype="application/json")
