#!flask/bin/python
from flask import Flask, jsonify, request, Response
from jsonrpcserver import method, dispatch
from app import app

#app = Flask(__name__)
secondary_url = ["http://localhost:80/", "http://localhost:8080/"]

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
    return jsonify({'tasks': messages})


@app.route('/messages', methods=['POST'])
def create_task():
    req = request.get_data().decode()
    print(req)
    response = dispatch(req)
    print(Response(response.http_status, mimetype="application/json"))
    return Response(str(response), response.http_status, mimetype="application/json")
    #print(str(response.))
    #return str(response)
