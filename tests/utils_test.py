import pytest
from utils import Posts, Comments, Bookmarks

@pytest.fixture()
def post_dao():
    posts_instance = Posts("data/data.json")
    return posts_instance

@pytest.fixture()
def comments_dao():
    comments_instance = Comments("data/comments.json")
    return comments_instance

@pytest.fixture()
def bookmarks_dao():
    bookmarks_instance = Bookmarks("data/bookmarks.json")
    return bookmarks_instance

comments_key_should_be = {"post_id", "commenter_name", "comment", "pk"}
posts_key_should_be = {"poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"}

class TestUtils:

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
        posts = post_dao.search_posts('природа')
        assert type(posts) == list, "Возвращается не список"
        assert len(posts) > 0, "Возвращает пустой список"
        assert set(posts[0].keys()) == posts_key_should_be, "Неверный список ключей"

    def test_get_tag_from_post(self,post_dao):
        post = post_dao.get_post_by_id(1)
        tags = post_dao.get_tag_from_post(post)
        assert type(tags) == list, "Возвращает не список"
        assert len(tags) > 0, "Пустой список"
        assert tags[0] == '#еда', "Возвращает неверный тег"

class TestComments:

    def test_get_all_comments(self, comments_dao):
        comments = comments_dao.get_all_comments()
        assert type(comments) == list, "Возвращает не словарь"
        assert len(comments) > 0, "Возвращает пустой список"
        assert set(comments[0].keys()) == comments_key_should_be, "Неверный список ключей"

    def test_get_comments_by_post_id(self, comments_dao):
        comment = comments_dao.get_comments_by_post_id(1)
        assert type(comment) == list, "Возвращает не список"
        assert len(comment) > 0, "Возвращает пустой список"
        assert set(comment[0].keys()) == comments_key_should_be, "Неверный список ключей"


class TestBookmarks:

    def test_get_bookmarks(self, bookmarks_dao):
        bookmarks = bookmarks_dao.get_bookmarks()
        assert type(bookmarks) == list, "Возвращает не список"
        assert len(bookmarks) > 0, "Возвращает пустой список"
        assert set(bookmarks[0].keys()) == posts_key_should_be, "Неверный список ключей"

    def test_save_bookmarks(self, bookmarks_dao):
        bookmarks = bookmarks_dao.get_bookmarks()
        bookmarks_dao.save_bookmarks(bookmarks)
        assert type(bookmarks) == list, "Возвращает не список"
        assert len(bookmarks) > 0, "Возвращает пустой список"
        assert set(bookmarks[0].keys()) == posts_key_should_be, "Неверный список ключей"

    def test_add_bookmarks(self, bookmarks_dao, post_dao):
        bookmarks = bookmarks_dao.get_bookmarks()
        len_first = len(bookmarks)
        post = post_dao.get_post_by_id(1)
        bookmarks_dao.add_bookmarks(post)
        bookmarks = bookmarks_dao.get_bookmarks()
        len_second = len(bookmarks)
        assert len_second > len_first, "Закладка не добавлена"
        assert type(bookmarks) == list, "Возвращает не список"
        assert len(bookmarks) > 0, "Возвращает пустой список"
        assert set(bookmarks[0].keys()) == posts_key_should_be, "Неверный список ключей"

    def test_delete_bookmarks(self, bookmarks_dao, post_dao):
        bookmarks = bookmarks_dao.get_bookmarks()
        len_first = len(bookmarks)
        post = post_dao.get_post_by_id(1)
        bookmarks_dao.delete_bookmarks(post['pk'])
        bookmarks = bookmarks_dao.get_bookmarks()
        len_second = len(bookmarks)
        assert len_first > len_second, "Закладка не удалена"
        assert type(bookmarks) == list, "Возвращает не список"
        assert len(bookmarks) > 0, "Возвращает пустой список"
        assert set(bookmarks[0].keys()) == posts_key_should_be, "Неверный список ключей"
