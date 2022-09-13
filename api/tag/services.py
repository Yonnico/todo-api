from flask import url_for
import copy

from api.tag.db import all_tags

from api.tag.validation import validate_title, validate_color

#FOR CONTROLLER

def get_tag_by_id(tag_id):
    tag = list(filter(lambda t: t['id'] == tag_id, all_tags))
    if len(tag):
        return tag[0]
    return None

def get_all_tags():
    tags = copy.deepcopy(all_tags)
    return tags

def make_public_tag(tag):
    new_tag = {}
    for field in tag:
        if field == 'id':
            new_tag['uri'] = url_for('get_tag', tag_id=tag['id'], _external=True)
        else:
            new_tag[field] = tag[field]
    return new_tag


def private_validate_tag(title, color, required):
    if required or title != None:
        if not validate_title(title):
            return False
    if required or color != None:
        if not validate_color(color):
            return False
    return True


def private_add_tag(title, color):
    id = all_tags[-1]['id'] + 1
    tag = {
        'id': id,
        'title': title,
        'color': color
    }
    all_tags.append(tag)
    return make_public_tag(tag)

#FOR VIEW

def get_tag_by_id_with_uri(tag_id):
    tag = get_tag_by_id(tag_id)
    if tag != None:
        return make_public_tag(tag)
    return None

def get_all_tags_with_uri():
    tags = get_all_tags()
    return list(map(make_public_tag, tags))


def validate_and_add_tag(title, color):
    if not private_validate_tag(title, color, True):
        return None
    return private_add_tag(title, color)


def validate_and_change_tag(tag_id, title, color):
    tag = get_tag_by_id(tag_id)
    if not tag:
        return {'status': 0, 'value': None}
    if not private_validate_tag(title, color, False):
        return {'status': 1, 'value': None}
    if title != None:
        tag['title'] = title
    if color != None:
        tag['color'] = color
    return {'status': 2, 'value': make_public_tag(tag)}

def remove_tag(tag_id):
    tag = get_tag_by_id(tag_id)
    if tag != None:
        return all_tags.remove(tag)
    return False