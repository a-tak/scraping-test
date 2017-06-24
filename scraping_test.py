#!/usr/bin/python3
# coding: UTF-8
import requests
from result_info import ResultInfo
from bs4 import BeautifulSoup

class Main():
    def execute(self):
        results = []
        results = self.get_yamada()
        results.extend(self.get_joshin())

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

    def get_joshin(self):
        results = []
        urls = []

        urls.append("http://joshinweb.jp/game/40519/4902370535709.html")
        urls.append("http://joshinweb.jp/game/40519/4902370535716.html")

        for url in urls:
            result_info = ResultInfo()
            
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "html.parser")
            result_info.title = soup.select("title")[0].text.strip()

            result_info.result = True
            result_info.note = "Not Foud"
            for element in soup.select(".fsL"):
                result_info.note = result_info.note + element.text.strip()
                if (element.text.strip() == "販売休止中です"):
                    result_info.result = False
                    break

            result_info.url = url

            results.append(result_info)

        return results
if __name__ == "__main__":
    main_obj = Main()
    main_obj.execute()