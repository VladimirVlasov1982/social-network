import logging
from flask import Flask, render_template, request, url_for, redirect, jsonify
from utils import Posts


# Создаем логирование
logging.basicConfig(filename='logs/api.log', format='%(asctime)s [%(levelname)s] %(message)s', encoding='utf-8',
                    level=logging.INFO)

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
post_dao = Posts()



@app.route('/')
def page_posts():
    # Страница постов.
    posts = post_dao.get_all_posts()
    len_posts = len(posts)
    return render_template('index.html', posts=posts, len_posts=len_posts)


@app.route('/posts/<int:post_id>')
def page_post(post_id):
    # Страница одного поста.
    post = post_dao.get_post_by_id(post_id)
    comments = post_dao.get_comments_by_post_id(post_id)
    len_comments = len(comments)
    return render_template('post.html', post = post, comments=comments, len_comments=len_comments)


@app.route("/seek")
def page_search_main():
    # Страница поиска.
    logging.info(f"Запрос ")
    response = request.args.get('get_seek')
    posts = post_dao.get_all_posts()
    if response:
        posts = post_dao.search_posts(response)
    len_posts = len(posts)
    return render_template('search.html', posts=posts, len_posts=len_posts, response=response)


@app.route('/users/<username>')
def page_user_posts(username):
    # Все посты одного пользователя.
    posts = post_dao.get_posts_by_user(username)
    return render_template('user-feed.html', posts=posts)


@app.errorhandler(404)
def pageNoteFound(error):
    # Обработчик 404. Страница не найдена.
    return render_template('page404.html'), 404


@app.route('/api/posts')
def api_posts():
    # Полный список постов в виде JSON-списка.
    logging.info(f"Запрос {url_for('api_posts')}")
    posts = post_dao.get_all_posts()
    return jsonify(posts)


@app.route('/api/posts/<int:post_id>')
def api_post_by_id(post_id):
    # Возвращает один пост в виде JSON-словаря.
    logging.info(f"Запрос {url_for('api_post_by_id', post_id=post_id)}")
    post = post_dao.get_post_by_id(post_id)
    return jsonify(post)


if __name__ == "__main__":
    app.run(debug=True)

