import pytest
from utils import Posts
from app import app


@pytest.fixture()
def post():
    post_instance = Posts()
    return post_instance

key_should_be = {"poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"}


class TestApiPosts:

    def test_api_posts(self):
        """Тестируем эндпоинт GET /api/posts. Проверяет возвращение списка и соответствие ключей."""
        response = app.test_client().get('/api/posts')
        assert type(response.json) == list, "Возвращается не список"
        assert response.json[0].keys() == key_should_be, "Неверный список ключей"

    def test_api_post_by_id(self,post):
        """Тестируем эндпоинт GET /api/posts/<post_id>. Проверяет возвращение словаря и соответствие ключей."""
        response = app.test_client().get('/api/posts/1')
        assert type(response.json) == dict, "Возвращает не словарь"
        assert response.json.keys() == key_should_be, "Неверный список ключей"

