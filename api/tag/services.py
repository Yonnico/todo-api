from flask import url_for

from api.tag.db import all_tags


def find_tag_by_id(tag_id):
     return list(filter(lambda t: t['id'] == tag_id, all_tags))


def make_public_tag(tag):
    new_tag = {}
    for field in tag:
        if field == 'id':
            new_tag['uri'] = url_for('get_tag', tag_id = tag['id'], _external=True)
        else:
            new_tag[field] = tag[field]
    return new_tag


def url_for_all_tags(tags):
    return list(map(make_public_tag, tags))


def url_for_tag(tag):
    return make_public_tag(tag)


def get_all_tags():
    return all_tags


def create_id_for_tag():
    return all_tags[-1]['id'] + 1


def add_tag(tag):
    return all_tags.append(tag)


def remove_tag(tag):
    return all_tags.remove(tag)