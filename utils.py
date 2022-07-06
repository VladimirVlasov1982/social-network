import json
from json import JSONDecodeError


class Posts:
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
            return "Файл не удается пеобразовать"

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


class Comments:

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


class Bookmarks:

    def __init__(self, path):
        self.path = path

    def get_bookmarks(self):
        """Загрузка данных из закладок"""
        with open(self.path, 'r', encoding='utf-8') as file:
            bookmarks = json.load(file)
            return bookmarks

    def save_bookmarks(self, bookmarks):
        # Сохраняем закладки
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(bookmarks, file, ensure_ascii=False, indent=4)

    def add_bookmarks(self, post):
        """Сохраняем пост в закладках"""
        bookmarks = self.get_bookmarks()
        bookmarks.append(post)
        self.save_bookmarks(bookmarks)

    def delete_bookmarks(self, post_id):
        """Удаляем пост из закладок"""
        bookmarks = self.get_bookmarks()
        for index, book in enumerate(bookmarks):
            if book['pk'] == post_id:
                del bookmarks[index]
                break
        self.save_bookmarks(bookmarks)
