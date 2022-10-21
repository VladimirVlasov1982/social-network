from flask import Blueprint, url_for, render_template, redirect
from .dao.bookmarks_dao import BookmarksDAO
from ..posts.dao.posts_dao import PostsDAO
from ..posts.views import posts_blueprint
import logging

bookmarks_blueprint = Blueprint("bookmarks_blueprint", __name__, template_folder="templates")

post_dao = PostsDAO('./data/data.json')
bookmarks_dao = BookmarksDAO('./data/bookmarks.json')

@bookmarks_blueprint.route('/bookmarks')
def page_bookmarks():
    # Страница закладок
    tags = post_dao.get_tag_from_post
    bookmarks = bookmarks_dao.get_bookmarks()
    return render_template("bookmarks.html", bookmarks=bookmarks, tags=tags)


@bookmarks_blueprint.route('/bookmarks/add/<int:post_id>', methods=['GET', 'POST'])
def page_add_bookmarks(post_id):
    logging.info("Добавление закладки")
    # Добавление постов в закладки
    post = post_dao.get_post_by_id(post_id)
    bookmarks_dao.add_bookmarks(post)
    return redirect('/', code=302)


@bookmarks_blueprint.route('/bookmarks/remove/<int:post_id>')
def page_delete_bookmarks(post_id):
    logging.info("Удаление закладки")
    # Удаление поста из закладок
    bookmarks_dao.delete_bookmarks(post_id)
    return redirect('/', code=302)