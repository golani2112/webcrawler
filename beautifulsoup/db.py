
from pymongo import MongoClient
from datetime import datetime, timedelta
import random
import os
import requests
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient


def connecttodb():
    client = MongoClient()
    db = client["Scraper"]
    collection = db["Links"]
    return collection


def savetodb(url, collection, source_Link):
    try:
        r = requests.get(url, timeout=10)
        if not documentInDatabase(r.url, collection):
            soup = bs(r.content)
            ran = ''.join(random.choices(k=10))
            with open('randomhtml/abc.html'.format(ran), 'w') as file:
                file.write(soup.prettify())
            file_path = ((os.path.dirname(__file__)) +
                         '/randomhtml/abc.html'.format(ran))
            link = {
                'Link': r.url,
                'Source_Link': source_Link,
                'Is_Crawled': False,
                'Last_Crawl_Dt': '',
                'Response_Status': r.status_code,
                'Content_type': r.headers['Content-Type'],
                'File_path': file_path,
                'Created_at': datetime.now()
            }
            collection.insert_one(link)
            print(r.url)
    except Exception as error:
        print(error)
        pass


def count(collection):
    return collection.count_documents({})


def documentInDatabase(url, collection):
    data = collection.find({"Link": url})
    for d in data:
        return True
    return False


def pendingLinks(collection):
    links = collection.find({"$or": [{"Is_Crawled": False}, {"Last_Crawl_Dt": {
                            "$lt": datetime.now() - timedelta(days=1)}}]})
    return links


def update(document, collection):
    collection.update_one({"_id": document["_id"]}, {"$set": {
        'Is_Crawled': True,
        'Last_Crawl_Dt': datetime.now()
    }})
