import json


class Posts:

    def get_all_posts(self):
        """Загружаем посты из json."""
        with open("data/data.json", "r", encoding="utf-8") as file:
            return json.load(file)

    def get_all_comments(self):
        """Загружаем комментарии из json."""
        with open('data/comments.json', "r", encoding="utf-8") as file:
            return json.load(file)

    def get_posts_by_user(self, username):
        """Получаем посты по имени пользователя."""
        posts = self.get_all_posts()
        posts_by_user = [post for post in posts if post['poster_name'].lower() == username.lower()]
        if posts_by_user:
            return posts_by_user
        else:
            raise ValueError("У пользователя не постов")

    def get_post_by_id(self, post_id):
        """Получаем посты по id."""
        posts = self.get_all_posts()
        for post in posts:
            if post["pk"] == post_id:
                return post

    def get_comments_by_post_id(self, post_id):
        """Получаем комментарии по id поста."""
        all_comments = self.get_all_comments()
        comments = [comment for comment in all_comments if comment['post_id'] == post_id]
        if comments:
            return comments
        else:
            raise ValueError("Комментариев нет")

    def search_posts(self, search):
        """Поиск постов по содержимому."""
        posts = self.get_all_posts()
        search_lower = search.lower()
        other_characters = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        search_posts = []
        for post in posts:
            for sign in other_characters:
                if sign in post['content']:
                    post['content'] = post['content'].replace(sign, "")
            if search_lower in post['content'].lower().split():
                search_posts.append(post)
        return search_posts

    def search_tag_post(self):
        """Поиск постов с тегами."""
        tag_posts = []
        posts = self.get_all_posts()
        for post in posts:
            if '#' in post['content']:
                tag_posts.append(post)
        return tag_posts

    def add_to_bookmarks(self, post):
        """Добавление поста в закладки"""
        with open('data/bookmarks.json', "w", encoding='utf-8') as file:
            json.dump(post, file, ensure_ascii=False)
