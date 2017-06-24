#!/usr/bin/python3
# coding: UTF-8
import requests
from result import ResultInfo
from bs4 import BeautifulSoup

class Main():
    def execute(self):
        results = None
        results = self.get_yamada()
        for result_info in results:
            print("{0},{1},{2},{3}".format(result_info.result, result_info.title, result_info.note, result_info.url))

    def get_yamada(self):
        results = []
        urls = []

        urls.append("http://www.yamada-denkiweb.com/1177992013")
        urls.append("http://www.yamada-denkiweb.com/1177991016")

        for url in urls:
            result_info = ResultInfo()
            
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "html.parser")
            result_info.title = soup.select("title")[0].text.strip()
            if (len(soup.select(".item-notice-block")) != 0):
                result_info.note = soup.select(".item-notice-block")[0].text.strip()
            else:
                result_info.note = "Not Foud"
            if (result_info.note != "好評につき売り切れました"):
                result_info.result = True
            else:
                result_info.result = False
            result_info.url = url
            
            results.append(result_info)

        return results

if __name__ == "__main__":
    main_obj = Main()
    main_obj.execute()