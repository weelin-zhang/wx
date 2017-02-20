#encoding=utf8
from flask import request,redirect,render_template
from app import app,db
from .admin import admin
from .girl import girl
app.register_blueprint(admin,url_prefix='/admin')
import re,time,json
from .plugs.face import ImageInfoFormat 
from .plugs import send,receive,search_music,weather,qiushibaike
from .plugs import models
pic_info_save_dict={}

app.register_blueprint(admin,url_prefix='/admin')
app.register_blueprint(girl,url_prefix='/girl')

@app.route('/')
def home():
    #obj = models.Session.query(models.Solution).first()
    return redirect('/admin/')

@app.route('/test/',methods=['GET'])
def test():
	print app.config['HUMOR_KEYS']
	print app.config['DEVICE_KEYS']
	return 'test page'


@app.route('/hander/',methods=['GET','POST'])
def hander():
	if request.method=='GET':
	    #return 'just test'
	    wx_data = request.args.to_dict()
	    print wx_data
	    return wx_data['echostr']
	
	client_info = request.get_data()
	print client_info
	deal_result = receive.deal_data(client_info)
	if not deal_result:print '获取类型错误';return 'success'
	touser,fromuser= deal_result.FromUserName,deal_result.ToUserName
	if isinstance(deal_result,receive.SubscribeMsg):
		#return send.send_text(touser,fromuser,'欢迎来的啊Weelin_Zhang订阅号,想听音乐的话可以输入music+空格+音乐名\n或者输入music+空格+音乐名+空格+歌手')
		return send.send_text(touser,fromuser,app.config['WELCOME_INFO'])
		#从记录中删除
	if isinstance(deal_result,receive.UNSubscribeMsg):
		#加入记录
		return send.send_text(touser,fromuser,app.config['WELCOME_INFO'])

	if isinstance(deal_result,receive.TextMsg):
	    #return send.send_text(touser,fromuser,'test')
	    user_input_l = deal_result.Content.split()
	    if len(user_input_l)<=1 and str(user_input_l[0]) not in app.config['HUMOR_KEYS']:
		return send.send_text(touser,fromuser,app.config['REMIND_INFO'])
	    user_key = str(user_input_l[0])
	    #return send.send_text(touser,fromuser,str(len(user_input_l))+str(user_key))
	    if len(user_input_l) == 1 and user_key in app.config['HUMOR_KEYS']:
		houmors='\n'.join(qiushibaike.get5infos())+'\n'+u'***输入1获取更多***'
	    	return send.send_text(touser,fromuser,houmors)
	    elif user_key in app.config['WEATHER_KEYS']:
		weather_info = weather.get_weather_info(user_input_l[1].decode('utf-8'))
		if not weather_info:
	    	    return send.send_text(touser,fromuser,'输入正确城市名..')
		return send.send_text(touser,fromuser,weather_info)			
	    elif user_key in app.config['MUSIC_KEYS']:	
		if len(user_input_l)>=3:
			music_info = search_music.get_music(user_input_l[1],user_input_l[2])
		else:
			music_info = search_music.get_music(user_input_l[1])
		if not music_info:return send.send_text(touser,fromuser,'兄弟,有这首歌吗-_-')
		return send.send_music(touser,fromuser,music_info[1],music_info[1],'zbMMCEVEvO0py0JHAHKRIMQBTU0_07436wi2fLYqYwmKnVYpeoO3wkaCMLyfPJPn',music_info[0]+'_%s'%music_info[2],music_info[3])
	    elif user_key in app.config['DEVICE_KEYS']:
                trouble_key = user_input_l[1]
		if trouble_key == 'all':
		    all_objs = models.Session.query(models.Solution).order_by(models.Solution.type_id).all()
		    result = ''
		    if not all_objs:
		        return send.send_text(touser,fromuser,'无相关记录')
		    for index,obj in enumerate(all_objs,1):
                        result=result+str(index)+'-'+obj.troublename+'for'+obj.type.departname+'\n'+obj.solution+'\n'*2
                    return send.send_text(touser,fromuser,result)
		objs = models.Session.query(models.Solution).filter(models.Solution.troublename.like('%{}%'.format(trouble_key))).order_by(models.Solution.id).all()
		if not objs:
		    return send.send_text(touser,fromuser,'无相关记录,获取全部方案请输入4+空格+all')
		result = '与"{}"相关的故障解决方法\n'.format(trouble_key)
		for index,obj in enumerate(objs,1):
		    result=result+str(index)+'-'+obj.troublename+'for'+obj.type.departname+'\n'+obj.solution+'\n'*2	
		return send.send_text(touser,fromuser,result)
		#return send.send_text(touser,fromuser,'数据库没有数据')
	    else:
		return send.send_text(touser,fromuser,app.config['REMIND_INFO'])
	    return 'success'
	elif isinstance(deal_result,receive.ImgMsg):
	    if deal_result.PicUrl in pic_info_save_dict:
		return send.send_text(touser,fromuser,c.pic_info)
	    mediaid = deal_result.MediaId
	    #print touser,fromuser,mediaid
	    #return send.send_img(touser,fromuser,mediaid)#把用户发过来的图片发回去
	    c = ImageInfoFormat(deal_result.PicUrl)
	    c.start();
	    pic_info_save_dict['PicUrl'] = c.pic_info
	    return send.send_text(touser,fromuser,c.pic_info)
	    
	elif isinstance(deal_result,receive.VoiceMsg):
	    mediaid = deal_result.MediaId
	    #return send.send_voice(touser,fromuser,mediaid)#原路返回语音
	    return send.send_text(touser,fromuser,u'你声音真好听')	
	elif isinstance(deal_result,receive.VideoMsg):
	    mediaid = deal_result.MediaId
	    #print mediaid
	    return send.send_video(touser,fromuser,mediaid,'title','descraption')
	    return send.send_text(touser,fromuser,u'视频')	
	
	elif isinstance(deal_result,receive.LocationMsg):
	    return send.send_text(touser,fromuser,'位置:%s经度:%s纬度:%s'%(deal_result.Label,deal_result.Location_X,deal_result.Location_Y))	
	elif isinstance(deal_result,receive.LinkMsg):
	    return send.send_text(touser,fromuser,'链接消息')	


#obj = Session.query(Solution).first()
