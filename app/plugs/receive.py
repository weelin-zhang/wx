#encoding=utf8

import re,time




'''
文本消息
图片消息
语音消息
视频消息
链接消息
'''





regex_text = re.compile(r'<ToUserName><!\[CDATA\[(.*?)\].*<FromUserName><!\[CDATA\[(.*?)\].*<CreateTime>(.*?)<.*<MsgType><!\[CDATA\[(.*?)\].*<Content><!\[CDATA\[(.*?)\].*<MsgId>(.*?)<',re.S)

regex_img = re.compile(r'<ToUserName><!\[CDATA\[(.*?)\].*<FromUserName><!\[CDATA\[(.*?)\].*<CreateTime>(.*?)<.*<MsgType><!\[CDATA\[(.*?)\].*<PicUrl><!\[CDATA\[(.*?)\].*<MsgId>(.*?)</MsgId>.*MediaId><!\[CDATA\[(.*?)]',re.S)

regex_voice = re.compile(r'<ToUserName><!\[CDATA\[(.*?)\].*<FromUserName><!\[CDATA\[(.*?)\].*<CreateTime>(.*?)<.*<MsgType><!\[CDATA\[(.*?)\].*MediaId><!\[CDATA\[(.*?)\].*Format><!\[CDATA\[(.*?)\].*<MsgId>(.*?)</MsgId>.*Recognition><!\[CDATA\[(.*?)\].*',re.S)

regex_video = re.compile(r'<ToUserName><!\[CDATA\[(.*?)\].*<FromUserName><!\[CDATA\[(.*?)\].*<CreateTime>(.*?)<.*<MsgType><!\[CDATA\[(.*?)\].*MediaId><!\[CDATA\[(.*?)\].*ThumbMediaId><!\[CDATA\[(.*?)\].*<MsgId>(.*?)</MsgId>.*',re.S)

regex_location = re.compile(r'<ToUserName><!\[CDATA\[(.*?)\].*<FromUserName><!\[CDATA\[(.*?)\].*<CreateTime>(.*?)<.*<MsgType><!\[CDATA\[(.*?)\].*<Location_X>(.*?)</L.*<Location_Y>(.*?)</L.*<Scale>(.*?)</.*<Label><!\[CDATA\[(.*?)\].*<MsgId>(.*?)</MsgId>.*',re.S)

regex_subscribe = re.compile(r'<ToUserName><!\[CDATA\[(.*?)\].*<FromUserName><!\[CDATA\[(.*?)\].*<CreateTime>(.*?)<.*<MsgType><!\[CDATA\[(.*?)\].*Event><!\[CDATA\[(.*?)\].*EventKey><!\[CDATA\[(.*?)\].*',re.S)

regex_unsubscribe = re.compile(r'<ToUserName><!\[CDATA\[(.*?)\].*<FromUserName><!\[CDATA\[(.*?)\].*<CreateTime>(.*?)<.*<MsgType><!\[CDATA\[(.*?)\].*Event><!\[CDATA\[(.*?)\].*EventKey><!\[CDATA\[(.*?)\].*',re.S)

def deal_data(web_data):
    if len(web_data) == 0:
        return None
    if web_data.find('<MsgType><![CDATA[text]]></MsgType>')!=-1:#text
        return TextMsg(web_data)
    elif web_data.find('<MsgType><![CDATA[image]]></MsgType>')!=-1:#img
        return ImgMsg(web_data)
    elif web_data.find('<MsgType><![CDATA[voice]]></MsgType>')!=-1:#voice
        return VoiceMsg(web_data)
    elif web_data.find('<MsgType><![CDATA[video]]></MsgType>')!=-1 or web_data.find('<MsgType><![CDATA[shortvideo]]></MsgType>')!=-1 :#video
        return VideoMsg(web_data)
    elif web_data.find('<MsgType><![CDATA[location]]></MsgType>')!=-1 :#location
        return LocationMsg(web_data)
    elif web_data.find('<MsgType><![CDATA[link]]></MsgType>')!=-1 :#link
        return LinkMsg(web_data)
    elif web_data.find('<Event><![CDATA[subscribe]]></Event>')!=-1 :#subcribe
        return SubscribeMsg(web_data)

    elif web_data.find('<Event><![CDATA[unsubscribe]]></Event>')!=-1 :#unsubcribe
        return UNSubscribeMsg(web_data)

    else:
        return None



class TextMsg(object):
    def __init__(self, web_data):
        result_l = re.findall(regex_text,web_data)[0]
        self.ToUserName,self.FromUserName,self.CreateTime,self.MsgType,self.Content,self.MsgId = result_l[0],result_l[1],result_l[2],result_l[3],result_l[4],result_l[5]

class ImgMsg(object):
    def __init__(self, web_data):
        result_l = re.findall(regex_img,web_data)[0]
        self.ToUserName,self.FromUserName,self.CreateTime,self.MsgType,self.PicUrl,self.MsgId,self.MediaId = result_l[0],result_l[1],result_l[2],result_l[3],result_l[4],result_l[5],result_l[6]

class VoiceMsg(object):
    def __init__(self, web_data):
        result_l = re.findall(regex_voice,web_data)[0]
        self.ToUserName,self.FromUserName,self.CreateTime,self.MsgType,self.MediaId,self.Format,self.MsgId,self.Recognition = result_l[0],result_l[1],result_l[2],result_l[3],result_l[4],result_l[5],result_l[6],result_l[7]


class VideoMsg(object):
    def __init__(self, web_data):
        result_l = re.findall(regex_video,web_data)[0]
        self.ToUserName,self.FromUserName,self.CreateTime,self.MsgType,self.MediaId,self.ThumbMediaId,self.MsgId = result_l[0],result_l[1],result_l[2],result_l[3],result_l[4],result_l[5],result_l[6]


class LocationMsg(object):
    def __init__(self,web_data):
        result_l =  re.findall(regex_location,web_data)[0]
        self.ToUserName,self.FromUserName,self.CreateTime,self.MsgType,self.Location_X,self.Location_Y,self.Scale,self.Label,self.MsgId = result_l[0],result_l[1],result_l[2],result_l[3],result_l[4],result_l[5],result_l[6],result_l[7],result_l[8]


class LinkMsg(object):
    def __init__(self,web_data):
        pass


class SubscribeMsg(object):
    def __init__(self,web_data):
        result_l =  re.findall(regex_subscribe,web_data)[0]
        self.ToUserName,self.FromUserName,self.CreateTime,self.MsgType,self.Event,self.EventKey = result_l[0],result_l[1],result_l[2],result_l[3],result_l[4],result_l[5]


class UNSubscribeMsg(object):
    def __init__(self,web_data):
        result_l =  re.findall(regex_unsubscribe,web_data)[0]
        self.ToUserName,self.FromUserName,self.CreateTime,self.MsgType,self.Event,self.EventKey = result_l[0],result_l[1],result_l[2],result_l[3],result_l[4],result_l[5]

if __name__ == '__main__':
    pass
