from flask import jsonify, request, Response
from jsonrpcserver import method, dispatch
from app import app

messages = []


@method
def save_message(text):
    messages.append(text)
    print(text)


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
    return Response(str(response), response.http_status, mimetype="application/json")
