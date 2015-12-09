# -*- coding: utf-8 -*-

SUMO_HOMEPAGE_URL = 'http://www.sumo.or.jp/'
BASE_URL = 'http://www.sumo.or.jp/honbasho/main/hoshitori'
EACH_DAY_URL = 'http://www.sumo.or.jp/honbasho/main/torikumi?day=%d&rank=1'

GZIP_HEADER = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
    'Accept-Encoding': 'gzip,deflate,sdch',
#    'Accept-Language': 'ja,zh-TW;q=0.8,zh;q=0.6,en;q=0.4,en-US;q=0.2',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'www.sumo.or.jp',
    'Pragma': 'no-cache',
}

HEADER = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'www.sumo.or.jp',
    'Pragma': 'no-cache',
}

WIN_LOSE_TYPE_DICT = {
    u'\u767d\u4e38' : 0,         # 白丸
    u'\u9ED2\u4E38' : 1,         # 黑丸
    u'\u4E0D\u6226\u52DD' : 2,   # 不戰勝
    u'\u4E0D\u6226\u6557' : 3,   # 不戰敗
    u'\u4F11\u307F' : 4,         # 休み
    u'\u5F15\u5206' : 5,         # 引分
    u'\u75DB\u5206' : 6          # 痛分
}