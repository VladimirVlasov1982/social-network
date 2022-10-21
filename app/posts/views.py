from flask import Blueprint, render_template, request, url_for, jsonify
import logging
from .dao.posts_dao import PostsDAO
from .dao.comments_dao import CommentsDAO
from ..bookmarks.dao.bookmarks_dao import BookmarksDAO

posts_blueprint = Blueprint('posts_blueprint', __name__, template_folder="templates")

post_dao = PostsDAO('./data/data.json')
bookmarks_dao = BookmarksDAO('./data/bookmarks.json')
comments_dao = CommentsDAO('./data/comments.json')


@posts_blueprint.route('/')
def page_posts():
    # Страница постов.
    posts = post_dao.get_all_posts()
    tags = post_dao.get_tag_from_post
    bookmarks = bookmarks_dao.get_bookmarks()
    len_posts = len(bookmarks)
    return render_template('index.html', posts=posts, len_posts=1, tags=tags, len=len_posts)


@posts_blueprint.route('/posts/<int:post_id>')
def page_post(post_id):
    # Страница одного поста.
    post = post_dao.get_post_by_id(post_id)
    post['views_count'] += 1
    post_dao.save_post(post)
    comments = comments_dao.get_comments_by_post_id(post_id)
    tags = post_dao.get_tag_from_post
    len_comments = len(comments)
    return render_template('post.html', post=post, comments=comments, len_comments=len_comments, tags=tags)


@posts_blueprint.route("/seek")
def page_search():
    # Страница поиска поста по содержанию.
    response = request.args.get('get_seek')
    posts = post_dao.get_all_posts()
    tags = post_dao.get_tag_from_post
    if response:
        posts = post_dao.search_posts(response)
        tags = post_dao.get_tag_from_post
    len_posts = len(posts)
    return render_template('search.html', posts=posts, len_posts=len_posts, response=response, tags=tags)


@posts_blueprint.route('/users/<username>')
def page_user_posts(username):
    # Страница постов одного пользователя.
    posts = post_dao.get_posts_by_user(username)
    tags = post_dao.get_tag_from_post
    return render_template('user-feed.html', posts=posts, tags=tags)


@posts_blueprint.route('/api/posts')
def page_api_posts():
    # Страница постов в виде JSON-списка.
    logging.info(f"Запрос {url_for('posts_blueprint.page_api_posts')}")
    posts = post_dao.get_all_posts()
    return jsonify(posts)


@posts_blueprint.route('/api/posts/<int:post_id>')
def page_api_post_by_id(post_id):
    # Страница с одним постом в виде JSON-словаря.
    logging.info(f"Запрос {url_for('posts_blueprint.page_api_post_by_id', post_id=post_id)}")
    post = post_dao.get_post_by_id(post_id)
    return jsonify(post)


@posts_blueprint.route('/tag/<tagname>')
def page_post_by_tag(tagname):
    # Страница постов по одному тегу
    tags = post_dao.get_tag_from_post
    posts = post_dao.get_posts_by_tagname(tagname)
    return render_template('tag.html', tagname=f"#{tagname}", posts=posts, tags=tags)
