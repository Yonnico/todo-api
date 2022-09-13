from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth

from api.tag.services import get_tag_by_id_with_uri, remove_tag
from api.tag.services import validate_and_add_tag, get_all_tags_with_uri
from api.tag.services import validate_and_change_tag

from api.task.services import get_tasks_with_tags, get_tasks_with_uri
from api.task.services import get_task_by_id_with_tags, get_task_by_id_with_uri
from api.task.services import remove_task, validate_and_add_task
from api.task.services import validate_and_change_task

app = Flask(__name__)

auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'admin':
        return 'password'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    tasks = get_tasks_with_uri()
    with_tags = request.args.get('with-tags')
    if with_tags or with_tags == '':
        tasks = get_tasks_with_tags()
    return jsonify({'all_tasks': tasks})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    task = get_task_by_id_with_uri(task_id)
    if not task:
        abort(404)
    with_tags = request.args.get('with-tags')
    if with_tags or with_tags == '':
        task = get_task_by_id_with_tags(task_id)
    return jsonify(task)


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
@auth.login_required
def add_task():
    if not request.json:
        abort(400)
    task = validate_and_add_task(
        request.json.get('title', None),
        request.json.get('description', None)
    )
    if not task:
        abort(404)
    return jsonify(task)


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def change_task(task_id):
    if not request.json:
        abort(400)
    response = validate_and_change_task(
        task_id,
        request.json.get('title', None),
        request.json.get('description', None),
        request.json.get('done', None)
    )
    if response['status'] == 0:
        abort(404)
    if response['status'] == 1:
        abort(400)
    result = response['value']
    return jsonify(result)


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    result = remove_task(task_id)
    if result == False:
        abort(404)
    return jsonify({'result': True})


@app.route('/todo/api/v1.0/tags', methods=['GET'])
@auth.login_required
def get_tags():
    tags = get_all_tags_with_uri()
    return jsonify({'all_tags': tags})


@app.route('/todo/api/v1.0/tags/<int:tag_id>', methods=['GET'])
@auth.login_required
def get_tag(tag_id):
    tag = get_tag_by_id_with_uri(tag_id)
    if not tag:
        abort(404)
    return jsonify(tag)

@app.route('/todo/api/v1.0/tags', methods=['POST'])
@auth.login_required
def add_tag():
    if not request.json:
        abort(400)
    tag = validate_and_add_tag(
        request.json.get('title', None),
        request.json.get('color', None)
    )
    if not tag:
        abort(400)
    return jsonify(tag)


@app.route('/todo/api/v1.0/tags/<int:tag_id>', methods=['PUT'])
@auth.login_required
def change_tag(tag_id):
    if not request.json:
        abort(400)
    response = validate_and_change_tag(
        tag_id,
        request.json.get('title', None),
        request.json.get('color', None)
    )
    if response['status'] == 0:
        abort(404)
    if response['status'] == 1:
        abort(400)
    result = response['value']
    return jsonify(result)


@app.route('/todo/api/v1.0/tags/<int:tag_id>', methods=['DELETE'])
@auth.login_required
def delete_tag(tag_id):
    result = remove_tag(tag_id)
    if result == False:
        abort(404)
    return jsonify({'result': True})