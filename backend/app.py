'''
/app.py
-> main file of the flask app
'''

from flask import Flask, Response, jsonify, request
import json

from dataGen.queries import handleQuery
from dataGen.suggestions import getSuggestions

from database.setup import initDatabase
from database.fetchData import fetchCSV
from database.models import Project, Interaction

from utilities.scheduler.setup import initScheduler, cleanScheduler
from utilities.cors.setup import initCors
from utilities.ratelimit.setup import initRateLimiter, limiter

app = Flask(__name__)

initDatabase(app)
initCors(app)
initRateLimiter(app)
initScheduler(app)

# ==================================================
# routes
# ==================================================

@app.route('/projects', methods=['GET'])
def get_projects():
    data = [project.serialize() for project in Project.query.all()]
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    return Response(json_str, mimetype='application/json; charset=utf-8')

@app.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    return jsonify(Project.query.get_or_404(project_id).serialize())

@app.route('/random-projects/<int:count>', methods=['GET'])
def get_random_projects(count):
    from sqlalchemy import func
    data = [project.serialize() for project in Project.query.order_by(func.random()).limit(min(count,Project.query.count())).all()]
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    return Response(json_str, mimetype='application/json; charset=utf-8')

@app.route('/suggestions/<int:project_id>', methods=['GET'])
def get_suggestions(project_id):
    return jsonify(getSuggestions(Project.query.get_or_404(project_id)))

@app.route('/query', methods=['POST'])
@limiter.limit("20 per minute")
def handle_query():
    return jsonify(handleQuery(request.json))

@app.route('/fetch-csv')
@limiter.limit("20 per minute")
def fetch_csv():
    return fetchCSV()

@app.route('/user-activity', methods=['GET'])
@limiter.limit("20 per minute")
def get_user_activity():
    data = [interaction.serialize() for interaction in Interaction.query.all()]
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    return Response(json_str, mimetype='application/json; charset=utf-8')

@app.route('/')
def home():
    return """
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Geist', 'Segoe UI', system-ui, sans-serif;
            background-color: #080808;
            color: #e0e0e0;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            font-size: 16px;
        }
    </style>
    <body>Lastro Backend is running!</body>
    """
    
# ==================================================
# main
# ==================================================

if __name__ == '__main__':
    try:
        app.run(debug=True, use_reloader=False)
    finally:
        cleanScheduler()