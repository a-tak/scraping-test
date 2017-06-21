# coding: UTF-8
import requests
from bs4 import BeautifulSoup

url = "http://www.yamada-denkiweb.com/category/108/001/009/"

r = requests.get(url)

#soup = BeautifulSoup(r.text.encode(r.encoding), "html.parser")
soup = BeautifulSoup(r.content, "html.parser")

title_tag = soup.find("title")
urikire = soup.select(".item-wrapper .note")

print(title_tag)
print(urikire)
print("end")
