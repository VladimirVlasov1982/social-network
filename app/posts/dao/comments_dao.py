import json
from json import JSONDecodeError

class CommentsDAO:

    def __init__(self, path):
        self.path = path

    def get_all_comments(self):
        """Загружаем комментарии из json."""
        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)

    def get_comments_by_post_id(self, post_id):
        """Получаем комментарии по id поста."""
        all_comments = self.get_all_comments()
        comments = [comment for comment in all_comments if comment['post_id'] == post_id]
        if comments:
            return comments
        else:
            raise ValueError("Комментариев нет")
