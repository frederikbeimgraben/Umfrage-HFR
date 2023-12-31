#!/usr/bin/env python3
"""
API Server for the Survey App
"""

import os
import json
from flask import Flask, request, jsonify, send_from_directory
import importlib

from survey import Survey, JSON, SurveyError
from db import DataBase

import surveys

app = Flask(__name__, static_url_path='')
db = DataBase('survey')

@app.route('/')
def index() -> str:
    """Serve the index page"""
    
    return jsonify(
        {
            'status': 'not_implemented',
            'message': 'This endpoint is not implemented yet.'
        }
    ), 501
    

@app.route('/api/surveys')
def server_dir():
    """
    List the contents of <__file__ directory>/surveys/*.json
    """
    
    return jsonify(
        {
            'status': 'success',
            'message': 'Successfully listed surveys',
            'surveys': [
                survey.split('.')[0] for survey in os.listdir(
                    os.path.join(os.path.dirname(__file__), 'surveys')
                ) if survey.endswith('.json')
            ]
        }
    ), 200

SURVEYS = {}

def load_survey(survey_name: str) -> Survey:
    """
    Load the survey with the given name
    """
    global SURVEYS
    
    base_path = os.path.dirname(__file__)
    
    file_path = os.path.join(base_path, 'surveys', f'{survey_name}.json')
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'Could not find survey {survey_name}')
    
    with open(file_path) as f:
        survey = Survey(json.load(f))
        
    if not survey_name in SURVEYS:
        SURVEYS[survey_name] = survey
        
    return survey

@app.route('/api/surveys/<survey_name>')
def serve_survey(survey_name: str) -> JSON:
    """
    Serve the survey with the given name
    """
    
    try:
        survey = load_survey(survey_name)
    except FileNotFoundError:
        return jsonify(
            {
                'status': 'not_found',
                'message': 'The requested survey was not found on the server. If you entered the URL manually please check your spelling and try again.'
            }
        ), 404
        
    return jsonify(
        survey.to_frontend()
    ), 200
    
@app.route('/api/surveys/<survey_name>/eval', methods=['GET', 'POST'])
def eval_survey(survey_name: str) -> JSON:
    """
    Evaluate the survey with the given name
    """
    
    if request.method == 'GET':
        return jsonify(
            {
                'status': 'not_supported',
                'message': 'The requested method is not supported for this endpoint.'
            }
        ), 404
        
    if not request.is_json:
        return jsonify(
            {
                'status': 'not_supported',
                'message': 'The requested content type is not supported for this endpoint.'
            }
        ), 404
        
    if 'answers' not in request.json or 'ref' not in request.json:
        print(request.json)
        return jsonify(
            {
                'status': 'bad_request',
                'message': 'The request body is missing the required parameters.'
            }
        ), 400
    
    try:
        survey = load_survey(survey_name)
    except FileNotFoundError:
        return jsonify(
            {
                'status': 'not_found',
                'message': 'The requested survey was not found on the server. If you entered the URL manually please check your spelling and try again.'
            }
        ), 404
        
    try:
        ref = request.json['ref']
        answers = request.json['answers']
        evaluation = survey.eval(answers.values())
        
        try:
            if not survey_name in db:
                db.add_survey(survey_name, survey.questions, survey.targets)
                
            db.add_result(
                survey_name,
                answers.values(),
                [
                    t["result"] for t in evaluation    
                ],
                reference=ref)
        except Exception as e:
            pass
        
        return jsonify(
            evaluation
        ), 200
    except SurveyError as e:
        return jsonify(
            {
                'status': 'error',
                'message': str(e)
            }
        ), 501

# Set CORS headers for the main app
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

if __name__ == '__main__':
    # Make production-ready
    app.config['ENV'] = 'production'
    
    app.run(debug=False, host='0.0.0.0', port=8081)