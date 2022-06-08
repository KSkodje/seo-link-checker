#!/usr/bin/python

from lxml import html
from urllib.parse import urlparse
import requests


def normalize_url(url):
    parsed_url = urlparse(url)

    base_url = parsed_url.scheme + '://' + parsed_url.netloc + parsed_url.path
    if base_url[-1] == '/':
        base_url = base_url[:-1]
    if base_url[0] == '/':
        base_url = base_url[1:]

    return base_url.lower()


def get_urls_from_string(page_content, base_url):
    urls = []
    tree = html.fromstring(page_content)
    tree.make_links_absolute(base_url=base_url)
    for elem in tree.iter():
        if elem.tag == "a":
            url = elem.get("href")
            urls.append(url)
    return urls


def validate_response(resp, url):
    is_status_ok = resp.ok
    is_html = 'text/html' in resp.headers['content-type']
    if not is_status_ok:
        raise Exception(f"URL did not respond successfully.\n{resp.status_code}")
    if not is_html:
        raise Exception(f"{url} didn't return HTML response.")


def crawl_page(base_url, current_url, pages: dict):
    normalized_url = normalize_url(current_url)

    if normalized_url not in pages:
        pages[normalized_url] = 0

    base_url_netloc = urlparse(base_url).netloc
    current_url_netloc = urlparse(current_url).netloc
    is_internal_link = base_url_netloc == current_url_netloc
    if not is_internal_link:
        pages[current_url] = None
        return pages

    if pages[normalized_url] is None:
        return pages

    if pages[normalized_url] > 0:
        pages[normalized_url] += 1
        return pages

    resp = requests.get(normalized_url)

    try:
        validate_response(resp, current_url)
    except Exception as e:
        print(e)
        pages[normalized_url] = None
        return pages

    pages[normalized_url] += 1

    urls = get_urls_from_string(resp.content, base_url)

    for url in urls:
        # print(f"Crawling: {url}")
        crawl_page(base_url, url, pages)

    return pages
