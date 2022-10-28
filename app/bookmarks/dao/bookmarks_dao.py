import json
from json import JSONDecodeError


class BookmarksDAO:

    def __init__(self, path):
        self.path = path

    def get_bookmarks(self):
        """Загрузка данных из закладок"""
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                bookmarks = json.load(file)
                return bookmarks
        except FileNotFoundError:
            return "Файл не найден"
        except JSONDecodeError:
            return "Файл не удается преобразовать"

    def save_bookmarks(self, bookmarks):
        # Сохраняем закладки
        try:
            with open(self.path, "w", encoding="utf-8") as file:
                json.dump(bookmarks, file, ensure_ascii=False, indent=4)
        except FileNotFoundError:
            return "Файл не найден"
        except JSONDecodeError:
            return "Файл не удается преобразовать"

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