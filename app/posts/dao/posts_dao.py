import json
from json import JSONDecodeError


class PostsDAO:
    def __init__(self, path):
        self.path = path

    def get_all_posts(self):
        """Загружаем посты из json."""
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return "Файл не найден"
        except JSONDecodeError:
            return "Файл не удается преобразовать"

    def save_post(self,post_add):
        try:
            data = self.get_all_posts()
            for post in data:
                if post_add['pk'] == post['pk']:
                    post['views_count'] = post_add['views_count']
                    with open(self.path, 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False, indent=2)
                    return f"Пост {post} готов к записи"

        except FileNotFoundError:
            return "Файл не найден"
        except JSONDecodeError:
            return "Файл не удается преобразовать"

    def get_posts_by_user(self, username):
        """Получаем посты по имени пользователя."""
        posts = self.get_all_posts()
        posts_by_user = [post for post in posts if post['poster_name'].lower() == username.lower()]
        if posts_by_user:
            return posts_by_user
        else:
            raise ValueError("У пользователя нет постов")

    def get_post_by_id(self, post_id):
        """Получаем посты по id."""
        posts = self.get_all_posts()
        for post in posts:
            if post["pk"] == post_id:
                return post

    def search_posts(self, search):
        """Поиск постов по содержимому."""
        posts = self.get_all_posts()
        search_lower = search.lower()
        characters = '#,.!:'
        search_posts = []
        for post in posts:
            for sign in characters:
                new_str = post['content'].lower().replace(sign, "").split()
                for word in new_str:
                    if search_lower == word and post not in search_posts:
                        search_posts.append(post)
        return search_posts

    def get_posts_by_tagname(self, tagname):
        """Поиск постов с тегами."""
        tag_posts = []
        tagname = '#' + tagname
        posts = self.get_all_posts()
        for post in posts:
            if tagname in post['content'].split():
                tag_posts.append(post)
        return tag_posts

    def get_tag_from_post(self, post):
        """Получение тэга из поста"""
        tag = []
        for word in post['content'].split():
            if word[:1] == '#':
                tag.append(word)
        return tag

    def __repr__(self):
        return "объект класса Post"