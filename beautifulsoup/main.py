from db import connecttodb, count, pendingLinks, savetodb
from crawler import crawl
import concurrent.futures

url = "https://flinkhub.com/"
if __name__ == '__main__':
    collection = connecttodb()
    savetodb(url, collection, "")

    while True:
        if count(collection) >= 5000:
            print("Maximum limit Reached")
            break

        documents = pendingLinks(collection)
        all_crawled = True
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            try:
                for document in documents:
                    all_crawled = False
                    futures.append(executor.submit(
                        crawl, document, collection))
                for future in concurrent.futures.as_completed(futures):
                    future.result()
            except Exception as error:
                print(error)
                break
        if all_crawled:
            print("All links are crawled!")
            break
