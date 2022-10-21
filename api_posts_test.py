import pytest
from run import app

posts_key_should_be = {"poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"}

def test_api_posts():
    response = app.test_client().get('/api/posts')
    assert type(response.json) == list
    assert response.json[0].keys() == posts_key_should_be

def test_api_post_by_id():
    response = app.test_client().get('/api/posts/1')
    assert type(response.json) == dict
    assert response.json.keys() == posts_key_should_be

