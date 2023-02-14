import requests
from bs4 import BeautifulSoup


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
