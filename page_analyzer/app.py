from flask import Flask, request, redirect, render_template, flash, get_flashed_messages
import psycopg2
from datetime import datetime
from validators.url import url
from urllib.parse import urlparse
from dotenv import load_dotenv
import os


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
app = Flask(__name__)
app.secret_key = SECRET_KEY


def add_to_base(site_url):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    now = datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s)", (site_url, date))
    conn.commit()
    cursor.close()
    conn.close()
    

def get_database():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM urls ORDER BY id DESC")
    database = cursor.fetchall()
    cursor.close()
    conn.close()
    return database


def get_database_entry_by_id(id):
    all_sites = get_database()
    for i in all_sites:
        if int(i[0]) == int(id):
            return i


def get_id_by_url(url):
    all_sites = get_database()
    for i in all_sites:
        if i[1] == url:
            return i[0]


def find_same_url(site_url):
    all_sites = get_database()
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
    site_list = get_database()
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
        return redirect('/')
    if not url(site_url) or len(site_url) > 255:
        flash('Некорректный URL', 'danger')
        return redirect('/')
    add_to_base(site_url)
    id = get_id_by_url(site_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(f'/urls/{id}')


@app.route('/urls/<id>')
def get_url(id):
    id, name, raw_date = get_database_entry_by_id(id)
    date = raw_date.strftime("%Y-%m-%d")
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'single_site.html',
        id=id, name=name, date=date, messages=messages
    )
