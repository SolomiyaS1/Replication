
from flask import jsonify, request, Response
from jsonrpcserver import method, dispatch
from app import app
import time

messages = []


@method
def save_message(text):
    messages.append(text)

@app.route('/')
def index():
    return 'Secondary node is running...'


@app.route('/messages', methods=['GET'])
def get_tasks():
    return jsonify({'messages': messages})


@app.route('/messages', methods=['POST'])
def create_task():
    req = request.get_data().decode()
    time.sleep(10)
    response = dispatch(req)
    return Response(str(response), response.http_status, mimetype="application/json")
