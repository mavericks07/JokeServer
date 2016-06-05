# -*- coding: UTF-8 -*-
"""
Created on 2016/6/2

@author: mavericks
"""
from flask import jsonify, request, make_response
from bson.json_util import dumps
from . import server
from .. import mongo
from random import randint, randrange
import hashlib
import xml.etree.ElementTree as ET
import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')


#安卓客户端接口


@server.route('/get_joke', methods=['GET', 'POST'])
def get_joke():
    type = request.json['type']
    jokes = mongo.db.Joke.find({'type': type})
    jokes = jokes.skip(randint(0, jokes.count() - 5)).limit(7)
    jokes = dumps({'test': list(jokes)})
    return jokes


@server.route('/', methods=['GET', 'POST'])
def wechat_auth():
    if request.method == 'GET':
        token = 'test'
        data = request.args
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        print hashlib.sha1(s).hexdigest(), signature
        if hashlib.sha1(s).hexdigest() == signature:
            return make_response(echostr)
    else:
        rec = request.stream.read()
        xml_rec = ET.fromstring(rec)
        tou = xml_rec.find('ToUserName').text
        fromu = xml_rec.find('FromUserName').text
        content = xml_rec.find('Content').text
        xml_rep = "<xml>" \
                  "<ToUserName><![CDATA[%s]]></ToUserName>" \
                  "<FromUserName><![CDATA[%s]]></FromUserName>" \
                  "<CreateTime>%s</CreateTime>" \
                  "<MsgType><![CDATA[text]]></MsgType>" \
                  "<Content><![CDATA[%s]]></Content>" \
                  "<FuncFlag>0</FuncFlag>" \
                  "</xml>"
        response = make_response(xml_rep % (fromu, tou, str(int(time.time())), content))
        response.content_type = 'application/xml'
        return response
