from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth

from api.tag.services import find_tag_by_id, get_all_tags
from api.tag.services import create_id_for_tag, add_tag, remove_tag
from api.tag.services import url_for_all_tags, url_for_tag

from api.task.services import find_task_by_id, get_all_tasks
from api.task.services import create_id_for_task, add_task, remove_task
from api.task.services import url_for_all_tasks, url_for_task

from api.core.services import validate_len, validate_for_str
from api.core.services import validate_for_request


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
    tasks = get_all_tasks()
    url_for_all_tasks(tasks)
    return jsonify({'all_tasks': tasks})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    task = find_task_by_id(task_id)
    validate_len(task)
    task = task[0]
    url_for_task(task)
    return jsonify(task)


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
@auth.login_required
def create_task():
    if not request.json:
        abort(400)
    validate_for_request('title')
    if not validate_for_str(request.json['title']):
        abort(400)
    if 'description' in request.json :
        if not validate_for_str(request.json['description']):
            abort(400)
    id = create_id_for_task()
    task = {
        'id': id,
        'title': request.json['title'],
        'description': request.json.get('description', ''),
        'done': False
    }
    add_task(task)
    url_for_task(task)
    return jsonify(task)


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def change_task(task_id):
    task = find_task_by_id(task_id)
    validate_len(task)
    task = task[0]
    if not request.json:
        abort(400)
    if 'title' in request.json:
        if not validate_for_str(request.json['title']):
            abort(400)
    if 'description' in request.json:
        if not isinstance(request.json['description'], str):
            abort(400)
    if 'done' in request.json:
        if not isinstance(request.json['done'], bool):
            abort(400)

    task['title'] = request.json.get('title', task['title'])
    task['description'] = request.json.get('description', task['description'])
    task['done'] = request.json.get('done', task['done'])
    url_for_task(task)
    return jsonify(task)


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = find_task_by_id(task_id)
    validate_len(task)
    task = task[0]
    remove_task(task)
    return jsonify({'result': True})


@app.route('/todo/api/v1.0/tags', methods=['GET'])
@auth.login_required
def get_tags():
    tags = get_all_tags()
    url_for_all_tags(tags)
    return jsonify({'all_tags': tags})


@app.route('/todo/api/v1.0/tags/<int:tag_id>', methods=['GET'])
@auth.login_required
def get_tag(tag_id):
    tag = find_tag_by_id(tag_id)
    validate_len(tag)
    tag = tag[0]
    url_for_tag(tag)
    return jsonify(tag)

@app.route('/todo/api/v1.0/tags', methods=['POST'])
@auth.login_required
def create_tag():
    if not request.json:
        abort(400)
    validate_for_request('title')
    validate_for_request('color')
    if not validate_for_str(request.json['title']):
        abort(400)
    if not validate_for_str(request.json['color']):
        abort(400)
    id = create_id_for_tag()
    tag = {
        'id': id,
        'title': request.json['title'],
        'color': request.json['color']
    }
    add_tag(tag)
    url_for_tag(tag)
    return jsonify(tag)


@app.route('/todo/api/v1.0/tags/<int:tag_id>', methods=['PUT'])
@auth.login_required
def change_tag(tag_id):
    tag = find_tag_by_id(tag_id)
    validate_len(tag)
    tag = tag[0]
    if not request.json:
        abort(400)
    if 'title' in request.json:
        if not validate_for_str(request.json['title']):
            abort(400)
    if 'color' in request.json:
        if not validate_for_str(request.json['color']):
            abort(400)
    tag['title'] = request.json.get('title', tag['title'])
    tag['color'] = request.json.get('color', tag['color'])
    url_for_tag(tag)
    return jsonify(tag)


@app.route('/todo/api/v1.0/tags/<int:tag_id>', methods=['DELETE'])
@auth.login_required
def delete_tag(tag_id):
    tag = find_tag_by_id(tag_id)
    validate_len(tag)
    tag = tag[0]
    remove_tag(tag)
    return jsonify({'result': True})