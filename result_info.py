#!/usr/bin/python3
# coding: UTF-8


class ResultInfo():
    u"""結果格納クラス
    """
    def __init__(self):
        self._url = ""
        self._title = ""
        self._result = False
        self._note = ""
        
    u"""取得URL
    """
    @property
    def url(self):
        return self._url
    @url.setter
    def url(self, url):
        self._url = url
    
    u"""取得ページタイトル
    """
    @property
    def title(self):
        return self._title
    @title.setter
    def title(self,title):
        self._title = title

    u"""結果
    """
    @property
    def result(self):
        return self._result
    @result.setter
    def result(self,result):
        self._result = result
    
    U"""メモ
    """
    @property
    def note(self):
        return self._note
    @note.setter
    def note(self,note):
        self._note = note
