from api.task.db import all_tasks
from api.tag.db import all_tags
from api.task.services import get_all_tasks
from api.task_with_tag.db import tasks_with_tags


def tags_for_tasks():
    return list(map(relations, all_tasks))


    