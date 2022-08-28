from flask import url_for

from api.tag.db import all_tags


def find_tag_by_id(tag_id):
     return list(filter(lambda t: t['id'] == tag_id, all_tags))


def get_all_tags():
    return all_tags


def create_id_for_tag():
    return all_tags[-1]['id'] + 1


def add_tag(tag):
    return all_tags.append(tag)


def remove_tag(tag):
    return all_tags.remove(tag)