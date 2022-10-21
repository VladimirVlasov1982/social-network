import logging
from flask import Flask, render_template, request, url_for, redirect, jsonify
from app.bookmarks.views import bookmarks_blueprint
from app.posts.views import posts_blueprint

# Создаем логирование
logging.basicConfig(filename='logs/api.log', format='%(asctime)s [%(levelname)s] %(message)s', encoding='utf-8',
                    level=logging.INFO, filemode='w')

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

app.register_blueprint(posts_blueprint)
app.register_blueprint(bookmarks_blueprint)

@app.errorhandler(404)
def pageNoteFound(error):
    # Обработчик 404. Страница не найдена.
    return render_template('page404.html', len=len), 404


@app.errorhandler(500)
def pageInternalServerError(error):
    # Обработчик 500. Ошибки на стороне сервера.
    return render_template('page500.html', len=len), 500



if __name__ == "__main__":
    app.run()
