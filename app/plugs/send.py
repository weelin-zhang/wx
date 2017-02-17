#encoding=utf8

import re,time


reply_text_tp = '''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%s]]></Content>
</xml>
'''


reply_img_tp = '''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[image]]></MsgType>
<Image>
<MediaId><![CDATA[%s]]></MediaId>
</Image>
</xml>
'''

reply_voice_tp='''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[voice]]></MsgType>
<Voice>
<MediaId><![CDATA[%s]]></MediaId>
</Voice>
</xml>
'''

reply_video_tp='''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[video]]></MsgType>
<Video>
<MediaId><![CDATA[%s]]></MediaId>
<Title><![CDATA[%s]]></Title>
<Description><![CDATA[%s]]></Description>
</Video>
</xml>
'''
reply_music_tp='''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[music]]></MsgType>
<Music>
<Title><![CDATA[%s]]></Title>
<Description><![CDATA[%s]]></Description>
<MusicUrl><![CDATA[%s]]></MusicUrl>
<HQMusicUrl><![CDATA[%s]]></HQMusicUrl>
<ThumbMediaId><![CDATA[%s]]></ThumbMediaId>
</Music>
</xml>
'''

def send_text(touser,fromuser,content):
    return reply_text_tp%(touser,fromuser,int(time.time()),content)

def send_img(touser,fromuser,mediaid):
    return reply_img_tp%(touser,fromuser,int(time.time()),mediaid)

def send_voice(touser,fromuser,mediaid):
    return reply_voice_tp%(touser,fromuser,int(time.time()),mediaid)

def send_video(touser,fromuser,mediaid,title='',description=''):
    return reply_video_tp%(touser,fromuser,int(time.time()),mediaid,title,description)

def send_music(touser,fromuser,MusicUrl,HQMusicUrl,ThumbMediaId,Title='music title',Description='music decription'):
    #print reply_music_tp%(touser,fromuser,int(time.time()),Title,Description,MusicUrl,HQMusicUrl,ThumbMediaId)

    return reply_music_tp%(touser,fromuser,int(time.time()),Title,Description,MusicUrl,HQMusicUrl,ThumbMediaId)
