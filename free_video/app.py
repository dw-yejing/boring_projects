from flask import Flask, render_template, request, url_for, current_app, send_from_directory
import os
from src.service.qq import get_search_list, get_series

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/search_list', methods=['GET', 'POST'])
def search_list():
    keywords = request.values.get("q")
    videos = get_search_list.get_list(keywords)
    return render_template('search_list.html', videos=videos)


@app.route('/detail', methods=['GET', 'POST'])
def detail():
    url = request.values.get("url")
    series = get_series.get_series(url)
    return render_template('detail.html', series=series)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found(error):
    return render_template("500.html"), 500


@app.errorhandler(503)
def page_not_found(error):
    return render_template("500.html"), 503


@app.errorhandler(Exception)
def page_not_found(error):
    return render_template("500.html"), 500


if __name__ == '__main__':
    app.run()
