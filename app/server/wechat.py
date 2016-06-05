# -*- coding: UTF-8 -*-
"""
Created on 2016/6/5

@author: mavericks
"""
from random import randint
import pymongo
import requests


class Mass:
    def __init__(self):
        self.appid = 'wx32645fda15b1bbfd'
        self.secret = 'b9ad2788bb91d7b10566ddd6da79c2a8'
        self.token = self.get_token()
        self.title = ''
        self.content = ''
        self.img_path = ''
        self.thumb_media_id = self.get_thumb_media_id()
        self.media_id = ''
        self.group_id = 0
        self.get_joke()
        # self.get_token()
        # self.get_token()
        # self.get_thumb_media_id()
        # self.get_group_id()
        # self.get_media_id()

    def get_joke(self):
        conn = pymongo.MongoClient()
        doc = conn.test_db.Joke
        jokes = doc.find()
        joke = jokes.skip(randint(0, jokes.count() - 1)).limit(1)[0]
        self.title = joke['title']
        self.content = joke['content']

    def get_token(self):
        url = 'https://api.weixin.qq.com/cgi-bin/token'
        params = {
            'grant_type': 'client_credential',
            'appid': self.appid,
            'secret': self.secret
        }
        resp = requests.get(url=url, params=params)
        resp = resp.json()
        self.token = resp['access_token']
        print self.token
        return self.token

    def get_thumb_media_id(self):
        url = 'https://api.weixin.qq.com/cgi-bin/media/upload'
        image_path = '../static/images/happy.png'
        params = {
            'access_token': self.token,
            'type': 'image'
        }
        file = {
            'media': open(image_path, 'rb')
        }
        resp = requests.post(url=url, params=params, files=file).json()
        self.thumb_media_id = resp['media_id']
        return self.thumb_media_id

    def get_group_id(self):
        url = 'https://api.weixin.qq.com/cgi-bin/groups/get'
        params = {
            'access_token': self.token
        }
        resp = requests.get(url=url, params=params).json()
        groups = resp['groups']
        for group in groups:
            if group['count'] != 0:
                self.group_id = group['id']
        return self.group_id

    def get_media_id(self):
        url = 'https://api.weixin.qq.com/cgi-bin/media/uploadnews'
        params = {
            'access_token': self.token
        }
        data = {
            'access_token': self.token,
            'articles': [
                {
                    "thumb_media_id": self.thumb_media_id,
                    "author": "mavericks",
                    "title": u"每日笑话",
                    "content": self.content,
                    "show_cover_pic": "1"
                }
            ]
        }
        resp = requests.post(url=url, data=data).json()
        print resp
        self.media_id = resp['media_id']
        print self.media_id
        return self.media_id

    def send(self):
        url = 'https://api.weixin.qq.com/cgi-bin/message/mass/sendall'
        params = {
            'filter': {
                'is_to_all': False,
                'group_id': self.get_group_id(),
            },
            'mpnews': {
                'media_id': self.get_media_id()
            },
            'msgtype': 'mpnews'
        }

m = Mass()
m.get_media_id()
