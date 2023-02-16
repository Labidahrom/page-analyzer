from flask import Flask, request, redirect, render_template, \
    flash, url_for
import psycopg2
from psycopg2.extras import NamedTupleCursor
from datetime import datetime
from urllib.parse import urlparse
from dotenv import load_dotenv
import os
import requests
from page_analyzer.url import validate_url
from page_analyzer.page import prepare_seo_data

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
app = Flask(__name__)
app.secret_key = SECRET_KEY


def add_to_url_checks_table(id, status_code, title, h1, description):
    date = datetime.now().strftime("%Y-%m-%d")
    conn = psycopg2.connect(DATABASE_URL)
    with conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute("INSERT INTO url_checks (url_id, status_code,"
                           " title, h1, description, created_at) VALUES "
                           "(%s, %s, %s, %s,  %s, %s)",
                           (id, status_code, title, h1, description, date))
            conn.commit()


@app.route('/')
def get_index():
    return render_template(
        'index.html')


@app.route('/urls')
def get_urls():
    conn = psycopg2.connect(DATABASE_URL)
    with conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute("SELECT DISTINCT ON (id) * FROM urls LEFT"
                           " JOIN (SELECT url_id, status_code,"
                           " created_at AS last_check_date FROM"
                           " url_checks ORDER BY id DESC) AS checks ON"
                           " urls.id = checks.url_id ORDER BY id DESC;")
            site_list = cursor.fetchall()
    return render_template(
        'site_list.html',
        site_list=site_list
    )


@app.post('/urls')
def post_urls():
    parse_url = urlparse(request.form.get("url"))
    site_url = f'{parse_url.scheme}://{parse_url.hostname}'
    if validate_url(site_url):
        flash('Некорректный URL', 'danger')
        return render_template('index.html'), 422
    conn = psycopg2.connect(DATABASE_URL)
    with conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute('SELECT * FROM urls WHERE name = %s', (site_url,))
            entry = cursor.fetchall()
    if entry:
        flash('Страница уже существует', 'info')
        return redirect(url_for('get_url', id=entry[0][0]))
    date = datetime.now().strftime("%Y-%m-%d")
    conn = psycopg2.connect(DATABASE_URL)
    with conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute("INSERT INTO urls (name, created_at) "
                           "VALUES (%s, %s)", (site_url, date))
            conn.commit()
            cursor.execute('SELECT id FROM urls WHERE name = %s', (site_url,))
            [(id,)] = cursor.fetchall()
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url', id=id))


@app.post('/urls/<id>/checks')
def post_url_check(id):
    conn = psycopg2.connect(DATABASE_URL)
    with conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute('SELECT * FROM urls WHERE id = %s', (id,))
            [(id, url, date)] = cursor.fetchall()
    try:
        status_code, title, h1, description = prepare_seo_data(url)
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('get_url', id=id))
    add_to_url_checks_table(id, status_code, title, h1, description)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_url', id=id))


@app.route('/urls/<id>')
def get_url(id):
    conn = psycopg2.connect(DATABASE_URL)
    with conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute('SELECT * FROM urls WHERE id = %s', (id,))
            [(id, name, date)] = cursor.fetchall()
            cursor.execute('SELECT * FROM url_checks WHERE url_id = %s '
                           'ORDER BY id DESC', (id,))
            site_checks = cursor.fetchall()
    return render_template(
        'single_site.html',
        id=id, name=name, date=date, site_checks=site_checks)
