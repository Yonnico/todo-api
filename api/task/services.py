from flask import url_for
from api.task.db import all_tasks


def find_task_by_id(task_id):
    return list(filter(lambda t: t['id'] == task_id, all_tasks))


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


def create_id_for_task():
    return all_tasks[-1]['id'] + 1


def add_task(task):
    return all_tasks.append(task)

def remove_task(task):
    return all_tasks.remove(task)