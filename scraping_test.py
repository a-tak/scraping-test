#!/usr/bin/python3
# coding: UTF-8
import requests
from result_info import ResultInfo
from bs4 import BeautifulSoup
from datetime import datetime
from slack import Slack
import yaml
import time

class Main():
    def execute(self):
        results = []
        results = self.get_yamada()
        results.extend(self.get_joshin())
        results.extend(self.get_nojima())
        results.extend(self.get_yodobashi())
        results.extend(self.get_nintendo())
        results.extend(self.get_rakutenbooks())
        results.extend(self.get_sofmap())

        yamlfile = "./setting.yaml"
        with open(yamlfile, "rt") as fp:
            text = fp.read()

        setting = yaml.safe_load(text)

        print(setting["slack-url"])
        print(setting["slack-username"])
        print(setting["slack-to"])

        slack = Slack()

        notices = []
        for result_info in results:
            print("{0},{1},{2},{3}".format(result_info.result, result_info.title, result_info.url, result_info.note))
            if (result_info.result == True):
                notices.append(result_info)
            ##テスト用に無条件に飛ぶようにしている
            #slack.send(setting["slack-url"], "{2} {0} : {1}".format(result_info.title, result_info.url, setting["slack-to"]), setting["slack-username"])

        for notice in notices:
            slack.send(setting["slack-url"], "{2} {0} : {1}".format(notice.title, notice.url, setting["slack-to"]), setting["slack-username"])

    def get_result(self, urls, target_element, target_str, *, search_mode=0):
        u""" HTMLパース
        search_mode = 0 文字列有無での判断
                    = 1 画像URL有無での判断(「在庫無し」の画像など)
        """
        results = []

        for url in urls:
            print("{1}:処理中…{0}".format(url, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

            result_info = ResultInfo()
            
            r = requests.get(url, timeout=15)
            soup = BeautifulSoup(r.content, "html.parser")

            result_info.title = soup.select("title")[0].text.strip()
            result_info.url = url

            if (search_mode==0):
                self.get_textsearch_result(soup, target_element, target_str, result_info)
            elif (search_mode==1):
                self.get_imgsearch_result(soup, target_element, target_str, result_info)
            else:
                raise NotImplementedError("Not Implement this search_mode")

            results.append(result_info)

            #1秒待つ
            time.sleep(1)

        return results

    def get_textsearch_result(self, soup, target_element, target_str, result_info):
        u"""指定テキストが存在する事を確認
        """
        result_info.result = True
        result_info.note = ""
        for element in soup.select(target_element):
            got_str = element.text.strip()
            result_info.note = result_info.note + got_str
            if (got_str == target_str):
                result_info.result = False
                break
        return result_info   

    def get_imgsearch_result(self, soup, target_element, target_str, result_info):
        u"""指定画像が存在する事を確認。target_strに画像URLを指定。
        """
        result_info.result = True
        result_info.note = ""
        for element in soup.select(target_element):
            got_str = element.attrs["src"].strip()
            result_info.note = result_info.note + got_str
            if (got_str == target_str):
                result_info.result = False
                break
        return result_info   

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

    def get_yodobashi(self):
        results = []
        urls = []

        urls.append("http://www.yodobashi.com/product/100000001003431566/")
        urls.append("http://www.yodobashi.com/product/100000001003431565/")

        return self.get_result(urls, ".salesInfo", "予定数の販売を終了しました")

    def get_nintendo(self):
        results = []
        urls = []

        urls.append("https://store.nintendo.co.jp/customize.html")

        return self.get_result(urls, "#custoize_toCart > span > button > span", "SOLD OUT")
        
    def get_rakutenbooks(self):
        results = []
        urls = []

        urls.append("http://books.rakuten.co.jp/rb/14647222/")
        urls.append("http://books.rakuten.co.jp/rb/14779136/")
        urls.append("http://books.rakuten.co.jp/rb/14647221/")
        urls.append("http://books.rakuten.co.jp/rb/14655635/")
        urls.append("http://books.rakuten.co.jp/rb/14655634/")

        return self.get_result(urls, "#purchaseBox > div > div > div.availability.s22 > div.status-area.clearfix > div.status-text > div.status-heading > span", "ご注文できない商品*")

    def get_sofmap(self):
        results = []
        urls = []

        urls.append("http://www.sofmap.com/product_detail.aspx?sku=13266081&gid=GF44010000")
        urls.append("http://www.sofmap.com/product_detail.aspx?sku=13266080&gid=GF44010000")

        return self.get_result(urls, ".product-detail-zaikocoment img", "/images/system_icon/zaiko06.gif", search_mode=1)

if __name__ == "__main__":
    main_obj = Main()
    main_obj.execute()