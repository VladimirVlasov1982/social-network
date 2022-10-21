import pytest
from app.bookmarks.dao.bookmarks_dao import BookmarksDAO
from app.posts.dao.posts_dao import PostsDAO


@pytest.fixture()
def post_dao():
    posts_instance = PostsDAO('data/data.json')
    return posts_instance

@pytest.fixture()
def bookmarks_dao():
    bookmarks_instance = BookmarksDAO("data/bookmarks.json")
    return bookmarks_instance

posts_key_should_be = {"poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"}

class TestBookmarksDAO:

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

