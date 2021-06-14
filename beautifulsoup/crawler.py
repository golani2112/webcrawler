from db import count, savetodb, update
import requests
from bs4 import BeautifulSoup as bs
from db import savetodb


def find_index(temp_url):
    if ".com" in temp_url:
        return temp_url.find(".com")
    elif ".co" in temp_url:
        return temp_url.find(".co")
    elif ".org" in temp_url:
        return temp_url.find(".org")
    elif ".us" in temp_url:
        return temp_url.find(".us")
    elif ".net" in temp_url:
        return temp_url.find(".net")
    elif ".blog" in temp_url:
        return temp_url.find(".blog")
    elif ".io" in temp_url:
        return temp_url.find(".io")
    elif ".biz" in temp_url:
        return temp_url.find(".biz")


def crawl(document, collection):
    update(document, collection)
    response = get(document["Link"], 10)
    links = getValidLinks(response)
    for link in links:
        if count(collection) >= 5000:
            raise Exception("Maximum Limit Reached")
        savetodb(link, collection, document["Link"])


def get(url, timeout):
    return requests.get(url, timeout=timeout)


def getValidLinks(response):
    links = []
    soup = bs(response.content, 'html5lib')
    href = soup.find_all('a', href=True)

    for href in href:
        if href.get('href').startswith("#") or href.get('href').startswith("tel:") or href.get('href').startswith("javascript:;") or href.get('href').startswith(" "):
            continue

        if href.get('href').startswith("https://") or href.get('href').startswith("http://"):
            links.append(href.get('href'))
            continue

        if href.get('href').startswith("/"):
            temp_url = response.url
            temp_index = find_index(temp_url)
            newurl = temp_url.replace(
                temp_url[temp_index:], "") + href.get('href').replace("/", "")
            links.append(newurl)

    return links
