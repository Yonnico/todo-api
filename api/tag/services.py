from flask import url_for, request

from api.tag.db import all_tags

from api.tag.validation import validate_title, validate_color


def get_tag_by_id(tag_id):
    tag = list(filter(lambda t: t['id'] == tag_id, all_tags))
    if len(tag):
        return tag[0]
    return None


def make_public_tag(tag):
    new_tag = {}
    for field in tag:
        if field == 'id':
            new_tag['uri'] = url_for('get_tag', tag_id=tag['id'], _external=True)
        else:
            new_tag[field] = tag[field]
    return new_tag


def url_for_all_tags(tags):
    return list(map(make_public_tag, tags))


def url_for_tag(tag):
    return make_public_tag(tag)


def get_all_tags():
    return all_tags


def remove_tag(tag_id):
    tag = get_tag_by_id(tag_id)
    if tag != None:
        return all_tags.remove(tag)
    return False

def validate_and_add_tag(title, color):
    if not private_validate_tag(title, color):
        return None
    return private_add_tag(title, color)


def private_validate_tag(title, color):
    if not request.json:
        return None
    if 'title' not in request.json:
        return None
    if 'color' not in request.json:
        return None
    if 'title' in request.json:
        if not validate_title(title):
            return None
    if 'color' in request.json:
        if not validate_color(color):
            return None
    return True


def private_add_tag(title, color):
    id = all_tags[-1]['id'] + 1
    tag = {
        'id': id,
        'title': title,
        'color': color
    }

    all_tags.append(tag)
    return tag


def validate_and_change_tag(tag_id, title, color):
    tag = get_tag_by_id(tag_id)
    if not tag:
        return {'status': 0, 'value': None}
    if not request.json:
        return {'status': 1, 'value': "No request"}
    if title is not None and not validate_title(title):
        return {'status': 1, 'value': title}
    if color is not None and not validate_color(color):
        return {'status': 1, 'value': color}
    if title is not None:
        tag['title'] = title
    if color is not None:
        tag['color'] = color
    return {'status': 2, 'value': tag}