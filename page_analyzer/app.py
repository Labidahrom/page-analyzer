from flask import Flask, request, redirect, render_template, \
    flash, get_flashed_messages, url_for
import psycopg2
from datetime import datetime
from validators.url import url
from urllib.parse import urlparse
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
app = Flask(__name__)
app.secret_key = SECRET_KEY


def connect_to_database():
    conn = psycopg2.connect(DATABASE_URL)
    return conn.cursor(), conn


def get_date():
    return datetime.now().strftime("%Y-%m-%d")


def prepare_seo_data(url):
    session = requests.session()
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) "
                             "Gecko/20100101 Firefox/60.0",
               "Accept": "text/html,application/xhtml+xml,"
                         "application/xml;q=0.9,*/*;q=0.8"}
    page = session.get(url, headers=headers)
    page.raise_for_status()
    status_code = page.status_code
    soup = BeautifulSoup(page.content, "html.parser")
    tags = [('title', {}), ('h1', {}), ('meta', {"name": "description"})]
    tags_text = {'title': '', 'h1': '', 'meta': ''}
    for tag, conditions in tags:
        node = soup.find(tag, conditions)
        if node:
            if tag == 'meta':
                tags_text[tag] = node.attrs.get("content", "")
            else:
                tags_text[tag] = node.get_text()
    return status_code, tags_text['title'], tags_text['h1'], \
        tags_text['meta']


def add_to_url_checks_table(id, status_code, title, h1, description):
    date = get_date()
    cursor, connection = connect_to_database()
    cursor.execute("INSERT INTO url_checks (url_id, status_code, title, "
                   "h1, description, created_at) VALUES (%s, %s, %s, %s,"
                   " %s, %s)", (id, status_code, title, h1, description,
                                date))
    connection.commit()
    cursor.close()
    connection.close()


@app.route('/')
def get_index():
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'index.html', messages=messages
    )


@app.route('/urls')
def get_urls():
    cursor, connection = connect_to_database()
    cursor.execute("SELECT DISTINCT ON (id) * FROM urls LEFT"
                   " JOIN (SELECT url_id, status_code,"
                   " created_at AS last_check_date FROM"
                   " url_checks ORDER BY id DESC) AS checks ON"
                   " urls.id = checks.url_id ORDER BY id DESC;")
    site_list = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template(
        'site_list.html',
        site_list=site_list
    )


@app.post('/urls')
def post_urls():
    cursor, connection = connect_to_database()
    parse_url = urlparse(request.form.to_dict()['url'])
    site_url = f'{parse_url.scheme}://{parse_url.hostname}'
    if not url(site_url) or len(site_url) > 255:
        flash('Некорректный URL', 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template(
            'index.html', messages=messages
        ), 422
    cursor.execute('SELECT * FROM urls WHERE name = %s', (site_url,))
    entry = cursor.fetchall()
    if entry:
        flash('Страница уже существует', 'info')
        return redirect(url_for('get_url', id=entry[0][0]))
    date = get_date()
    cursor.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s)",
                   (site_url, date))
    connection.commit()
    cursor.execute('SELECT id FROM urls WHERE name = %s', (site_url,))
    [(id,)] = cursor.fetchall()
    cursor.close()
    connection.close()
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url', id=id))


@app.post('/urls/<id>/checks')
def post_url_check(id):
    cursor, connection = connect_to_database()
    cursor.execute('SELECT * FROM urls WHERE id = %s', (id,))
    [(id, url, date)] = cursor.fetchall()
    try:
        status_code, title, h1, description = prepare_seo_data(url)
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('get_url', id=id))
    add_to_url_checks_table(id, status_code, title, h1, description)
    cursor.close()
    connection.close()
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_url', id=id))


@app.route('/urls/<id>')
def get_url(id):
    cursor, connection = connect_to_database()
    cursor.execute('SELECT * FROM urls WHERE id = %s', (id,))
    [(id, name, date)] = cursor.fetchall()
    cursor.execute('SELECT * FROM url_checks WHERE url_id = %s '
                   'ORDER BY id DESC', (id,))
    site_checks = cursor.fetchall()
    cursor.close()
    connection.close()
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'single_site.html',
        id=id, name=name, date=date, messages=messages,
        site_checks=site_checks
    )
