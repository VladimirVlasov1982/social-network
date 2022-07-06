import logging
from flask import Flask, render_template, request, url_for, redirect, jsonify
from utils import Posts, Comments, Bookmarks

# Создаем логирование
logging.basicConfig(filename='logs/api.log', format='%(asctime)s [%(levelname)s] %(message)s', encoding='utf-8',
                    level=logging.INFO)

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
post_dao = Posts("data/data.json")
comments_dao = Comments('data/comments.json')
bookmarks_dao = Bookmarks('data/bookmarks.json')


@app.route('/')
def page_posts():
    # Страница постов.
    posts = post_dao.get_all_posts()
    tags = post_dao.get_tag_from_post
    bookmarks = bookmarks_dao.get_bookmarks()
    len_posts = len(bookmarks)
    return render_template('index.html', posts=posts, len_posts=1, tags=tags, len=len_posts)


@app.route('/posts/<int:post_id>')
def page_post(post_id):
    # Страница одного поста.
    post = post_dao.get_post_by_id(post_id)
    comments = comments_dao.get_comments_by_post_id(post_id)
    tags = post_dao.get_tag_from_post
    len_comments = len(comments)
    return render_template('post.html', post=post, comments=comments, len_comments=len_comments, tags=tags)


@app.route("/seek")
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


@app.route('/users/<username>')
def page_user_posts(username):
    # Страница постов одного пользователя.
    posts = post_dao.get_posts_by_user(username)
    tags = post_dao.get_tag_from_post
    return render_template('user-feed.html', posts=posts, tags=tags)


@app.errorhandler(404)
def pageNoteFound(error):
    # Обработчик 404. Страница не найдена.
    return render_template('page404.html', len=len), 404


@app.errorhandler(500)
def pageInternalServerError(error):
    # Обработчик 500. Ошибки на стороне сервера.
    return render_template('page500.html', len=len), 500


@app.route('/api/posts')
def page_api_posts():
    # Страница постов в виде JSON-списка.
    logging.info(f"Запрос {url_for('page_api_posts')}")
    posts = post_dao.get_all_posts()
    return jsonify(posts)


@app.route('/api/posts/<int:post_id>')
def page_api_post_by_id(post_id):
    # Страница с одним постом в виде JSON-словаря.
    logging.info(f"Запрос {url_for('page_api_post_by_id', post_id=post_id)}")
    post = post_dao.get_post_by_id(post_id)
    return jsonify(post)


@app.route('/tag/<tagname>')
def page_post_by_tag(tagname):
    # Страница постов по одному тегу
    tags = post_dao.get_tag_from_post
    posts = post_dao.get_posts_by_tagname(tagname)
    return render_template('tag.html', tagname=f"#{tagname}", posts=posts, tags=tags)


@app.route('/bookmarks')
def page_bookmarks():
    # Страница закладок
    tags = post_dao.get_tag_from_post
    bookmarks = bookmarks_dao.get_bookmarks()
    return render_template("bookmarks.html", bookmarks=bookmarks, tags=tags)


@app.route('/bookmarks/add/<int:post_id>')
def page_add_bookmarks(post_id):
    # Добавление постов в закладки
    post = post_dao.get_post_by_id(post_id)
    bookmarks_dao.add_bookmarks(post)
    return redirect(url_for('page_posts'), code=302)


@app.route('/bookmarks/remove/<int:post_id>')
def page_delete_bookmarks(post_id):
    # Удаление поста из закладок
    bookmarks_dao.delete_bookmarks(post_id)
    return redirect(url_for('page_posts'), code=302)


if __name__ == "__main__":
    app.run()
