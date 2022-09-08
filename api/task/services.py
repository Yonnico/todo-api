from flask import url_for, request

from api.task.db import all_tasks

from api.task.validation import validate_done, validate_title, validate_description


def get_task_by_id(task_id):
    task = list(filter(lambda t: t['id'] == task_id, all_tasks))
    if len(task):
        return task[0]
    return None


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


def url_for_all_tasks(tasks):
    return list(map(make_public_task, tasks))


def url_for_task(task):
    return make_public_task(task)


def get_all_tasks():
    return all_tasks


def remove_task(task_id):
    task = get_task_by_id(task_id)
    if task != None:
        return all_tasks.remove(task)
    return False


def validate_and_add_task(title, description):
    id = all_tasks[-1]['id'] + 1
    task = {
        'id': id,
        'done': False
    }
    if not request.json:
        return {'status': 1, 'value': "No request"}
    if not validate_title(title):
        return {'status': 1, 'value': title}
    if description is not None and not validate_description(description):
        return {'status': 1, 'value': description}
    task['title'] = title
    task['description'] = description
    all_tasks.append(task)
    return {'status': 2, 'value': task}


def validate_and_change_task(task_id, title, description, done):
    task = get_task_by_id(task_id)
    if not task:
        return {'status': 0, 'value': None}
    if not request.json:
        return {'status': 1, 'value': "No request"}
    if title is not None and not validate_title(title):
        return {'status': 1, 'value': title}
    if description is not None and not validate_description(description):
        return {'status': 1, 'value': description}
    if done is not None and not validate_done(done):
        return {'status': 1, 'value': done}
    if title is not None:
        task['title'] = title
    if description is not None:
        task['description'] = description
    if done is not None:
        task['done'] = done
    return {'status': 2, 'value': task}