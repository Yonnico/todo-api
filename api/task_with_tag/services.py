from api.task_with_tag.db import tasks_with_tags

from api.tag.services import get_tag_by_id_with_uri

#FOR CONTROLLER

def get_links_by_task_id(task_id):
    return list(filter(lambda t: t['task_id'] == task_id, tasks_with_tags))


def get_task_with_tags(task):
    task['tags'] = []
    links = get_links_by_task_id(task['id'])
    for link in links:
        tag = get_tag_by_id_with_uri(link['tag_id'])
        task['tags'].append(tag)
    return task
