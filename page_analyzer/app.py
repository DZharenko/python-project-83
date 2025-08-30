import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from .models import add_url, get_all_urls, get_url_by_id, validate_url

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/urls", methods=['POST'])
def urls_post():
    url = request.form.get('url', '').strip()
    
    # Валидация
    error = validate_url(url)
    if error:
        flash(error, 'danger')
        return render_template("index.html", url=url), 422
    
    try:
        url_id = add_url(url)
        return redirect(url_for('url_detail', id=url_id))
    except Exception:
        flash('Произошла ошибка при добавлении URL', 'danger')
        return render_template("index.html", url=url), 500
    

@app.route("/urls")
def urls_list():
    urls = get_all_urls()
    return render_template("urls.html", urls=urls)


@app.route("/urls/<int:id>")
def url_detail(id):
    url = get_url_by_id(id)
    if not url:
        flash('Страница не найдена', 'danger')
        return redirect(url_for('index'))
    
    return render_template("url.html", url=url)

# @app.route("/urls/<int:id>")
# def url_detail(id):
#     print(f"🔍 Запрос URL с ID: {id}")  # Отладочное сообщение
#     url = get_url_by_id(id)
    
#     if not url:
#         print("❌ URL не найден в базе данных")  # Отладочное сообщение
#         flash('Страница не найдена', 'danger')
#         return redirect(url_for('index'))
    
#     print(f"✅ Найден URL: {url}")  # Отладочное сообщение
#     return render_template("url.html", url=url)


if __name__ == "__main__":
    app.run(debug=True)