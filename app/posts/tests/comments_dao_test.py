import pytest
from app.posts.dao.comments_dao import CommentsDAO


@pytest.fixture()
def comments_dao():
    comments_instance = CommentsDAO("data/comments.json")
    return comments_instance

comments_key_should_be = {"post_id", "commenter_name", "comment", "pk"}

class TestComments:

    def test_get_all_comments(self, comments_dao):
        comments = comments_dao.get_all_comments()
        print(comments)
        assert type(comments) == list, "Возвращает не словарь"
        assert len(comments) > 0, "Возвращает пустой список"
        assert set(comments[0].keys()) == comments_key_should_be, "Неверный список ключей"

    def test_get_comments_by_post_id(self, comments_dao):
        comment = comments_dao.get_comments_by_post_id(1)
        assert type(comment) == list, "Возвращает не список"
        assert len(comment) > 0, "Возвращает пустой список"
        assert set(comment[0].keys()) == comments_key_should_be, "Неверный список ключей"

