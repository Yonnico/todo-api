from api.task_with_tag.db import tasks_with_tags
from api.tag.db import all_tags


def tags_for_tasks(tasks):
    return list(map(tags_for_task, tasks))


def tags_for_task(task):
    task['tags'] = []
    links = list(filter(lambda t: t['task_id'] == task['id'], tasks_with_tags))
    for link in links:
        tag = list(filter(lambda t: t['id'] == link['tag_id'], all_tags))
        task['tags'].append(tag)
    return task
