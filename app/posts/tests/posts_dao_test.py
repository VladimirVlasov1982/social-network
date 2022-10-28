import pytest
from app.posts.dao.posts_dao import PostsDAO


@pytest.fixture()
def post_dao():
    posts_instance = PostsDAO('data/data.json')
    return posts_instance

posts_key_should_be = {"poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"}



class TestPostsDAO:

    def test_get_all_posts(self, post_dao):
        posts = post_dao.get_all_posts()
        assert type(posts) == list, "Возвращается не список"
        assert len(posts) > 0, "Возвращается пустой список"
        assert set(posts[0].keys()) == posts_key_should_be, "Неверный список ключей"

    def test_get_posts_by_user(self, post_dao):
        posts = post_dao.get_posts_by_user("leo")
        assert type(posts) == list, "Возвращает не список"
        assert posts[0]['poster_name'] == 'leo', "Неверное имя пользователя"
        assert set(posts[0].keys()) == posts_key_should_be, "Неверный список ключей"

    def test_get_post_by_id(self, post_dao):
        post = post_dao.get_post_by_id(1)
        assert type(post) == dict, "Возвращает не словарь"
        assert post['pk'] == 1, "Возвращается неправильный пост"
        assert post.keys() == posts_key_should_be, "Неверный список ключей"

    def test_search_posts(self, post_dao):
        posts = post_dao.search_posts('кот')
        assert type(posts) == list, "Возвращается не список"
        assert len(posts) > 0, "Возвращает пустой список"
        assert set(posts[0].keys()) == posts_key_should_be, "Неверный список ключей"

    def test_get_tag_from_post(self,post_dao):
        post = post_dao.get_post_by_id(5)
        tags = post_dao.get_tag_from_post(post)
        assert type(tags) == list, "Возвращает не список"
        assert len(tags) > 0, "Пустой список"
        assert tags[0] == '#кот', "Возвращает неверный тег"