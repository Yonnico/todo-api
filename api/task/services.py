from flask import url_for
import copy

from api.task.db import all_tasks

from api.task.validation import validate_done, validate_title, validate_description
from api.task_with_tag.services import get_task_with_tags

#FOR CONTROLLER


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


def get_all_tasks():
    tasks = copy.deepcopy(all_tasks)
    return tasks


def private_validate_task(title, description, required):
    if required or title != None:
        if not validate_title(title):
            return False
    if description != None:
        if not validate_description(description):
            return False
    return True


def private_add_task(title, description):
    id = all_tasks[-1]['id'] + 1
    task = {
        'id': id,
        'title': title,
        'description': description,
        'done': False
    }
    all_tasks.append(task)
    return make_public_task(task)

#FOR VIEW

def get_task_by_id_with_tags(task_id):
    task = get_task_by_id(task_id)
    task = copy.deepcopy(task)
    if task != None:
        task = get_task_with_tags(task)
        return task
    return None


def get_task_by_id_with_uri(task_id):
    task = get_task_by_id(task_id)
    if task != None:
        task = make_public_task(task)
        return task
    return None


def get_tasks_with_uri():
    tasks = get_all_tasks()
    return list(map(make_public_task, tasks))


def get_tasks_with_tags():
    tasks = get_all_tasks()
    tasks = list(map(get_task_with_tags, tasks))
    return list(map(make_public_task, tasks))


def validate_and_add_task(title, description):
    if not private_validate_task(title, description, True):
        return None
    return private_add_task(title, description)


def validate_and_change_task(task_id, title, description, done):
    task = get_task_by_id(task_id)
    if not task:
        return {'status': 0, 'value': None}
    if not private_validate_task(title, description, False):
        return {'status': 1, 'value': None}
    if done != None:
        if not validate_done(done):
            return {'status': 1, 'value': 'done'}
    if title != None:
        task['title'] = title
    if description != None:
        task['description'] = description
    if done != None:
        task['done'] = done
    return {'status': 2, 'value': make_public_task(task)}


def remove_task(task_id):
    task = get_task_by_id(task_id)
    if task != None:
        return all_tasks.remove(task)
    return False