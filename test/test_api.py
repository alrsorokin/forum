import json
from datetime import datetime

import pytest
from forum.models import Section, Post, Comment
from forum.lib.const import ERRORS


def create_sections():
    sections = [
        {
            'theme': 'test theme1',
            'description': 'test_description1',
            'created_at': datetime.now()
        },
        {
            'theme': 'test theme2',
            'description': 'test_description2',
            'created_at': datetime.now()
        },
        {
            'theme': 'test theme3',
            'description': 'test_description3',
            'created_at': datetime.now()
        }
    ]
    for section in sections:
        Section(**section).save()


def create_posts():
    create_sections()
    posts = [
        {
            'theme': 'test theme1 post',
            'description': 'test_description1 post',
            'created_at': datetime.now(),
            'section_id': 1
        },
        {
            'theme': 'test theme2 post',
            'description': 'test_description2 post',
            'created_at': datetime.now(),
            'section_id': 2
        },
        {
            'theme': 'test theme3 post',
            'description': 'test_description3 post',
            'created_at': datetime.now(),
            'section_id': 3
        }
    ]
    for post in posts:
        Post(**post).save()


def test_health_check(client):
    response = client.get('/api/v1/health-check')
    assert response.status_code == 200
    assert response.data == b'OK'


def test_get_section_list(client, db):
    create_sections()
    response = client.get('/api/v1/sections')
    assert response.status_code == 200
    assert b'test_description3' in response.data


def test_get_section_empty_list(client):
    response = client.get('/api/v1/sections')
    assert response.status_code == 200
    assert not json.loads(response.data)


@pytest.mark.parametrize(
    "section_id, result",
    [(1, 'test theme1'), ("1", 'test theme1'), (2, 'test theme2')],
)
def test_get_section_by_id_success(client, db, section_id, result):
    create_sections()
    response = client.get(f'/api/v1/sections/{section_id}')
    assert response.status_code == 200
    assert result in response.data.decode()


def test_get_section_by_id_failed(client, db):
    create_sections()
    response = client.get('/api/v1/sections/98')
    assert response.status_code == 404
    assert ERRORS[404] in response.data.decode()


@pytest.mark.parametrize(
    "body",
    [{
        'theme': 'test theme',
        'description': 'test_description',
    }]
)
def test_create_section_success(client, body):
    body = json.dumps(body)
    response = client.post('/api/v1/sections', data=body, content_type='application/json')
    assert response.status_code == 201
    assert 'test theme' in response.data.decode()

    section = Section.query.first()
    assert section.theme == 'test theme'


@pytest.mark.parametrize(
    "body",
    [{
        'theme': '',
        'description': 'test_description',
    }, {
        'theme': 'test theme',
        'description': '',
    }, {
        'theme': 200 * 'test',
        'description': 200 * 'test',
    }],
)
def test_create_section_failed(client, body):
    body = json.dumps(body)
    response = client.post('/api/v1/sections', data=body, content_type='application/json')
    assert response.status_code == 400
    assert ERRORS[400] in response.data.decode()


@pytest.mark.parametrize(
    "body",
    [{
        'theme': 'new_theme',
        'description': 'new_description',
    }]
)
def test_update_section(client, db, body):
    create_sections()
    section_old = Section.query.get(1).json()
    body = json.dumps(body)
    response = client.put('/api/v1/sections/1', data=body, content_type='application/json')
    section_new = Section.query.get(1).json()
    assert response.status_code == 202
    assert not section_old['updated_at']
    assert section_new['updated_at']


def test_delete_section(client, db):
    create_sections()
    response = client.delete('/api/v1/sections/1')
    assert response.status_code == 204
    section = Section.query.get(1)
    assert not section


def test_get_posts(client, db):
    create_posts()
    response = client.get("/api/v1/sections/1/posts")
    assert response.status_code == 200
    assert b'test_description1 post' in response.data


@pytest.mark.parametrize(
    "post",
    [{
        'theme': 'test post theme',
        'description': 'test post description',
    }]
)
def test_create_post_success(client, db, post):
    create_sections()
    body = json.dumps(post)
    response = client.post("/api/v1/sections/1/posts", data=body, content_type='application/json')
    assert response.status_code == 201

    section = Section.query.get(1)
    assert len(section.posts) == 1
    assert section.posts[0].description == 'test post description'


@pytest.mark.parametrize(
    "post",
    [{
        'theme': '',
        'description': 'test_description',
    }, {
        'theme': 'test theme',
        'description': '',
    }, {
        'theme': 200 * 'test',
        'description': 200 * 'test',
    }]
)
def test_create_post_failed(client, db, post):
    create_sections()
    body = json.dumps(post)
    response = client.post("/api/v1/sections/1/posts", data=body, content_type='application/json')
    assert response.status_code == 400
    assert ERRORS[400] in response.data.decode()


def test_get_post(client, db):
    create_posts()
    post = Post.query.first()
    for i in range(5):
        Comment(text=f'test comment {i}', post=post, created_at=datetime.now())

    response = client.get("/api/v1/sections/1/posts/1")
    assert response.status_code == 200
    assert len(json.loads(response.data)['comments']) == 5


@pytest.mark.parametrize(
    "body",
    [{
        'theme': 'new_theme',
        'description': 'new_description',
    }]
)
def test_update_post(client, db, body):
    create_posts()
    post_old = Post.query.get(1).json()
    body = json.dumps(body)
    response = client.put("/api/v1/sections/1/posts/1", data=body, content_type='application/json')
    post_new = Post.query.get(1).json()

    assert response.status_code == 202
    assert not post_old['updated_at']
    assert post_new['updated_at']


def test_delete_post(client):
    create_posts()
    response = client.delete("/api/v1/sections/1/posts/1")
    assert response.status_code == 204
    post = Post.query.get(1)
    assert not post


@pytest.mark.parametrize(
    "comment",
    [{
        'text': 'comment1',
    }]
)
def test_create_comment_success(client, db, comment):
    create_posts()
    body = json.dumps(comment)
    response = client.post("/api/v1/sections/1/posts/1/comments",
                           data=body, content_type='application/json')

    assert response.status_code == 201
    post = Post.query.get(1)

    assert len(post.comments) == 1
    assert post.comments[0].text == 'comment1'
