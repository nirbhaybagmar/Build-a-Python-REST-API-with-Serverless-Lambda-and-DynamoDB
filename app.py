import os

import boto3

from flask import Flask, jsonify, request
app = Flask(__name__)

#USERS_TABLE = os.environ['USERS_TABLE']
client = boto3.client('dynamodb')


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/users/<string:formId>" , methods=['GET'])
def get_user(formId):
    resp = client.get_item(
        TableName= 'informationTable',
        Key={
            'formId': { 'S': formId }
        }
    )
    item = resp.get('Item')
    if not item:
        return jsonify({'error': 'form does not exist'}), 404

    return jsonify({
        'formId': item.get('formId').get('S'),
        'createdBy': item.get('createdBy').get('S'),
        'question' : item.get('question').get('S')
    })


@app.route("/users", methods=["POST"])
def create_user():
    formId = request.json.get('formId')
    createdBy = request.json.get('createdBy')
    question = request.json.get('question')
    if not formId or not createdBy:
        return jsonify({'error': 'Please provide formId '}), 400

    resp = client.put_item(
        TableName='informationTable',
        Item={
            'formId': {'S': formId },
            'createdBy': {'S': createdBy },
            'question': {'S': question },
        }
    )

    return jsonify({
        'formId': formId,
        'createdBy': createdBy,
        'question' : question
    })

@app.route("/res", methods=["POST"])
def insert_response():
    formId = request.json.get('formId')
    response = request.json.get('response')
    emailId = request.json.get('emailId')
    if not formId or not emailId:
        return jsonify({'error': 'Please provide formId and emailId '}), 400

    resp = client.put_item(
        TableName='responseTable',
        Item={
            'formId': {'S': formId },
            'response': {'S': response },
            'emailId': {'S': emailId },
        }
    )

    return jsonify({
        'formId': formId,
        'response': response,
        'emailId' : emailId
    })

@app.route("/res/<string:formId>" , methods=['GET'])
def get_response(formId):
    resp = client.get_item(
        TableName= 'responseTable',
        Key={
            'formId': { 'S': formId }
        }
    )
    item = resp.get('Item')
    if not item:
        return jsonify({'error': 'form does not exist'}), 404

    return jsonify({
        'formId': item.get('formId').get('S'),
        'response': item.get('response').get('S'),
        'emailId' : item.get('emailId').get('S')
    })
