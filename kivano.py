from bs4 import BeautifulSoup
import requests
import csv

CSV = "kivano.csv"
URL = "https://www.kivano.kg/sportivnoe-pitanie"
HOST = "https://www.kivano.kg/"


def get_html(URL, params=""):
    r = requests.get(URL, params=params, verify=False)
    return r


def get_content(html):
    soup = BeautifulSoup(html.text)
    items = soup.find_all("div", class_="list-view")

    proteins = []

    for item in items:
        proteins.append({
            "name": item.find("div", class_="item").find('div', class_='pull-right rel').find('a').get_text(strip=True),
            'price': item.find("div", class_="item").find('div', class_='pull-right rel').find("div", class_="listbox_price").get_text(strip=True),
            "text": item.find("div", class_="item").find("div", class_="product_text pull-left").text.strip(),
            'link': HOST + item.find('div', class_='listbox_img').find('a').get('href'),
            "image": item.find("div", class_="listbox_img").find("img").get("src")
        })
    return proteins

def save(items, path):
    with open(path, "a") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["name", "link", "text", "price", "image"])
        for item in items:
            writer.writerow([item["name"], item["price"], item["text"], item["link"], item["image"]])

def pagination():
    PAGINATION = input("pages ? :")
    PAGINATION = int(PAGINATION.strip())
    items = []
    html = get_html(URL)
    if html.status_code == 200:
        for page in range(1, PAGINATION + 1):
            print(f"page{page}is done")
            html = get_html(URL, params={"page": page})
            items.extend(get_content(html))
        save(items, CSV)
        print("parsing is done")
    else:
        print("parsing is break")


pagination()
