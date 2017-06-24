#!/usr/bin/python3
# coding: UTF-8
import requests
from result_info import ResultInfo
from bs4 import BeautifulSoup
from datetime import datetime
from slack import Slack
import yaml

class Main():
    def execute(self):
        results = []
        results = self.get_yamada()
        results.extend(self.get_joshin())
        results.extend(self.get_nojima())

        yamlfile = "./setting.yaml"
        with open(yamlfile, "rt") as fp:
            text = fp.read()

        setting = yaml.safe_load(text)

        print(setting["slack-url"])
        print(setting["slack-username"])

        slack = Slack()

        notices = []
        for result_info in results:
            print("{0},{1},{2},{3}".format(result_info.result, result_info.title, result_info.url, result_info.note))
            if (result_info.result == True):
                notices.append(result_info)

        for notice in notices:
            slack.send(setting["slack-url"], "{0} : {1}".format(notice.title, notice.url),setting["slack-username"])

    def get_result(self, urls, target_element, target_str):
        results = []

        for url in urls:
            print("{1}:処理中…{0}".format(url, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

            result_info = ResultInfo()
            
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "html.parser")
            result_info.title = soup.select("title")[0].text.strip()

            result_info.result = True
            result_info.note = ""
            for element in soup.select(target_element):
                result_info.note = result_info.note + element.text.strip()
                if (element.text.strip() == target_str):
                    result_info.result = False
                    break

            result_info.url = url

            results.append(result_info)

        return results
       

    def get_yamada(self):
        results = []
        urls = []

        urls.append("http://www.yamada-denkiweb.com/1177992013")
        urls.append("http://www.yamada-denkiweb.com/1177991016")

        return self.get_result(urls, ".item-notice-block", "好評につき売り切れました")

    def get_joshin(self):
        results = []
        urls = []

        urls.append("http://joshinweb.jp/game/40519/4902370535709.html")
        urls.append("http://joshinweb.jp/game/40519/4902370535716.html")

        return self.get_result(urls, ".fsL", "販売休止中です")

    def get_nojima(self):
        results = []
        urls = []

        urls.append("https://online.nojima.co.jp/Nintendo-HAC-S-KABAA-ESET-【NSW】-ニンテンドースイッチ本体-Joy-Con%28L%29-ネオンブルー-%28R%29-ネオンレッド（5年保証セット）-/2810000036439/1/cd/")
        urls.append("https://online.nojima.co.jp/Nintendo-HAC-S-KAAAA-ESET-【NSW】-ニンテンドースイッチ本体-Joy-Con%28L%29-%28R%29-グレー（5年保証セット）-/2810000036422/1/cd/")

        return self.get_result(urls, ".hassoumeyasu2", "完売御礼")
if __name__ == "__main__":
    main_obj = Main()
    main_obj.execute()