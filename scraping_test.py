#!/usr/bin/python3
# coding: UTF-8
import requests
from bs4 import BeautifulSoup

url = "http://www.yamada-denkiweb.com/category/108/001/009/"

r = requests.get(url)

soup = BeautifulSoup(r.content, "html.parser")

note_elements = soup.select(".item-wrapper .note")

for note_element in note_elements:
    print(note_element.text)
