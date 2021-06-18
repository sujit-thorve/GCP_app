# Copyright 2017, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Set up Flask stuff
"""
from flask import Blueprint, render_template
from flask import send_from_directory
from flask import request, redirect
from quiz.webapp import questions
from google.cloud import datastore
datastore_client = datastore.Client()
"""
configure blueprint
"""
webapp_blueprint = Blueprint(
    'webapp',
    __name__,
    template_folder='templates',
)


"""
Renders home page
"""
@webapp_blueprint.route('/')
def serve_home():
    return render_template('home.html')

"""
Serves static file with angular client app
"""
@webapp_blueprint.route('/search/')
def serve_client():
    #results=datastore.list_entities()
    query = datastore_client.query(kind='Question')
    limit=5
    times = query.fetch(limit=limit)
    return render_template('index.html',times=times)

"""
Serves static files used by angular client app
"""
@webapp_blueprint.route('/client/<path:path>')
def serve_client_files(path):
    return send_from_directory('webapp/static/client', path)

"""
Handles definition and storage of new questions
- GET method shows question entry form
- POST method save question
"""
@webapp_blueprint.route('/questions/add', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add.html', question={}, action='Add')
    elif request.method == 'POST':
        data = request.form.to_dict(flat=True)
        questions.save_question(data)
        return redirect('/', code=302)
    else:
        return "Method not supported for /questions/add"
