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
URLS_QUERY = "SELECT * FROM urls ORDER BY id DESC"


def add_to_url_table(site_url):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s)",
                   (site_url, date))
    conn.commit()
    cursor.close()
    conn.close()


def make_url_check(url):
    page = requests.get(url)
    status_code = page.status_code
    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find('title')
    h1 = soup.find('h1')
    description = None
    if title:
        title = title.get_text()
    if h1:
        h1 = h1.get_text()
    meta_search = soup.find_all("meta")
    for i in meta_search:
        if i.get('name') == 'description':
            description = i.get('content')
    return status_code, title, h1, description


def add_to_url_checks_table(id, status_code, title, h1, description):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO url_checks (url_id, status_code, title, "
                   "h1, description, created_at) "
                   "VALUES (%s, %s, %s, %s, %s, %s)",
                   (id, status_code, title, h1, description, date))
    conn.commit()
    cursor.close()
    conn.close()


def get_database(query):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(query)
    database = cursor.fetchall()
    cursor.close()
    conn.close()
    return database


def get_database_entry_by_id(id):
    all_sites = get_database(URLS_QUERY)
    for i in all_sites:
        if int(i[0]) == int(id):
            return i


def get_id_by_url(url):
    all_sites = get_database(URLS_QUERY)
    for i in all_sites:
        if i[1] == url:
            return i[0]


def find_same_url(site_url):
    all_sites = get_database(URLS_QUERY)
    for i in all_sites:
        if i[1] == site_url:
            return i


@app.route('/')
def get_index():
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'index.html', messages=messages
    )


@app.route('/urls')
def get_urls():
    join_urls_query = "SELECT DISTINCT ON (id) * FROM urls LEFT JOIN" \
                      " (SELECT url_id, status_code, created_at AS" \
                      " last_check_date FROM url_checks ORDER BY id DESC) AS" \
                      " checks ON urls.id = checks.url_id ORDER BY id DESC;" \

    site_list = get_database(join_urls_query)
    return render_template(
        'site_list.html',
        site_list=site_list
    )


@app.post('/urls')
def post_urls():
    parse_url = urlparse(request.form.to_dict()['url'])
    site_url = f'{parse_url.scheme}://{parse_url.hostname}'
    if find_same_url(site_url):
        flash('Страница уже существует', 'info')
        return redirect(url_for('get_index'))
    if not url(site_url) or len(site_url) > 255:
        flash('Некорректный URL', 'danger')
        return redirect(url_for('get_index'))
    add_to_url_table(site_url)
    id = get_id_by_url(site_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url', id=id))


@app.post('/urls/<id>/checks')
def post_url_check(id):
    try:
        id, url, date = get_database_entry_by_id(id)
        status_code, title, h1, description = make_url_check(url)
    except requests.exceptions.ConnectionError:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('get_url', id=id))

    add_to_url_checks_table(id, status_code, title, h1, description)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_url', id=id))


@app.route('/urls/<id>')
def get_url(id):
    id, name, date = get_database_entry_by_id(id)
    url_checks_query = f"SELECT * FROM url_checks WHERE url_id" \
                       f" = {id} ORDER BY id DESC"
    site_checks = get_database(url_checks_query)
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'single_site.html',
        id=id, name=name, date=date, messages=messages,
        site_checks=site_checks
    )
