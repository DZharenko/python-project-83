import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
from models import validate_url, add_url, get_url_by_id, get_all_urls, get_url_checks, add_url_check 

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/urls", methods=['POST'])
def urls_post():
    url = request.form.get('url', '').strip()
    
    error = validate_url(url)

    if error:
        flash(error, 'danger')
        return render_template("index.html", url=url), 422
    
    try:
        url_id = add_url(url)
        return redirect(url_for('url_detail', id=url_id))

    except Exception as e:
        flash(f'Произошла ошибка при добавлении URL: !!!{str(e)}', 'danger')
        return render_template("index.html", url=url), 500


@app.route("/urls/<int:id>")
def url_detail(id):
    url = get_url_by_id(id)
    if not url:
        flash('Страница не найдена', 'danger')
        return redirect(url_for('index'))
    
    checks = get_url_checks(id)
       
    return render_template("url_detail.html", url=url, checks = checks)


@app.route("/urls")
def urls_list():
    urls = get_all_urls()
    return render_template("urls.html", urls=urls)



@app.post("/urls/<id>/checks")
def url_checks(id):
    url = get_url_by_id(id)

    if not url:
        flash('Сайт не найден', 'danger')
        return redirect(url_for("urls_list"))
    
    try:
        add_url_check(id)
        flash("Страница успешно добавлена", 'success')
        return redirect(url_for('url_detail', id=id))
    except Exception as e:
        flash("Произошла ошибка при проверке", 'danger')

        return redirect(url_for('url_detail', id=id))    

        

if __name__ == "__main__":
    app.run(debug=True)