#!/usr/bin/python3
# coding: UTF-8

import requests
import json

class Slack():
    def send(self, url, msg, username):
        u""" Slackへメッセージ送信
        http://qiita.com/polikeiji/items/f8fa08331bd4a12f66df
        """
        requests.post(url, data = json.dumps({
            'text': msg, # 投稿するテキスト
            'username': username, # 投稿のユーザー名
            'icon_emoji': u':ghost:', # 投稿のプロフィール画像に入れる絵文字
            'link_names': 1, # メンションを有効にする
        }))


if __name__ == "__main__":
    main_obj = Slack()
    main_obj.send()    