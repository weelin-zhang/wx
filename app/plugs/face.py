#encoding=utf8
#!/usr/local/bin/python2.7

import urllib2,urllib
import json





class ImageInfoFormat(object):
	def __init__(self,img_url):
		self.__detect_url = "https://api-cn.faceplusplus.com/facepp/v3/detect"
		self.__sceneandobject_url = "https://api-cn.faceplusplus.com/imagepp/beta/detectsceneandobject"
		self.img_url = img_url
		self.pic_info = None


	def start(self):
		self.face_info()

	def face_info(self):
		values={

				"api_key":"qmeuyLEeWWLtRcgcJzs07Q8oLiLY0F5I",
				"api_secret":"9KGYLErpaXtAZTNw3z3_aGpE59TcHhK4",
				"image_url":self.img_url,
				"return_attributes":"gender,age,smiling,glass,headpose,facequality",
		}
		headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
		data = urllib.urlencode(values)
		request = urllib2.Request(self.__detect_url,data=data,headers=headers)
		try:
			response = urllib2.urlopen(request,timeout=2)
			r = response.read()
			faces_l = json.loads(r)['faces']#返回人物信息的列表
			if not faces_l:
				print u'不是人脸,场景检测'
				return self.object_info()
			self.face_info_format(faces_l)
		except Exception as e:
			print '1:',e
			self.pic_info = u'有毒' 



	def object_info(self):
		values={
				"api_key":"qmeuyLEeWWLtRcgcJzs07Q8oLiLY0F5I",
	            "api_secret":"9KGYLErpaXtAZTNw3z3_aGpE59TcHhK4",
	            "image_url":self.img_url,
			}

		headers={'User-Agent':'	Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'}
		data = urllib.urlencode(values)
		request = urllib2.Request(self.__sceneandobject_url,data=data,headers=headers)
		print self.__sceneandobject_url
		try:
			response = urllib2.urlopen(request,timeout=10)
			r = response.read()
			d_info = json.loads(r)
			self.object_info_format(d_info)
		except Exception as e:
			print 'fuck',e
			self.pic_info = '有毒1'
		#{u'time_used': 1427, u'image_id': u'30u+XVGYRxJB81r07llN/w==', u'objects': [{u'confidence': 44.363, u'value': u'Person'}], u'scenes': [], u'request_id': u'1483592470,3a5847eb-f106-4510-8a48-15182c8b47ef'}




	def face_info_format(self,face_l):
		if len(face_l)>1:self.pic_info = u'我一次只想看一个人...';return
		attributes = face_l[0]['attributes']#人物列表
		glass = attributes['glass']['value']#是否佩戴眼镜的分析结果，value的值为None/Dark/Normal。None代表不佩戴眼镜，Dark代表佩戴墨镜，Normal代表佩戴普通眼镜.
		gender = attributes['gender']['value']#Female/Male
		age = attributes['age']['value']#int
		smile_threshold = attributes['smile']['threshold']
		smile_val = attributes['smile']['value']
		#comment
		if glass=='Dark':glass_info = u'感觉酷酷的样子'
		elif glass=='Normal':glass_info = u'你眼镜太普通了,换墨镜吧'
		else:glass_info = u'戴个墨镜一起High...'
		if smile_val > 2*smile_threshold:smile_info=u'看你笑成什么了..'
		elif smile_val>smile_threshold and smile_threshold>40:smile_info=u'说句老实话你笑的挺好看'
		elif int(smile_val)/int(smile_threshold)==1:smile_info=u'好吧，我承认你在笑..'
		elif smile_val < smile_threshold:
		    smile_info=u'多笑笑吧，有好处'
		if gender=='Female':gender_info='girl'
		else:gender_info='man'
		reply_res = u'''Hi,%s
	你今年大概齐%s岁,
	%s
	%s
	'''%(gender_info,age,smile_info,glass_info)
		self.pic_info = reply_res
 


	#{u'time_used': 1427, u'image_id': u'30u+XVGYRxJB81r07llN/w==', u'objects': [{u'confidence': 44.363, u'value': u'Person'}], u'scenes': [], u'request_id': u'1483592470,3a5847eb-f106-4510-8a48-15182c8b47ef'}
	def object_info_format(self,d_info):
		pic_info=None
		scenes_l,objects=[],[]
		scenes_l=d_info['scenes']#列表有可能是空-场景
		objects = d_info['objects']#列表有可能是空-物品
		if not scenes_l:#没有场景
			if not objects:
				self.pic_info = u'什么都没有'
			else:
				self.pic_info = u'有点像一个%s'%(objects[0]['value'])
		else:#有场景
			if not objects:
				self.pic_info = u'有点像%s'%(scenes_l[0]['value'])

			else:
				self.pic_info = u'貌似有%s还有%s'%(scenes_l[0]['value'],objects[0]['value'])


if  __name__ == '__main__':
	u = 'http://s13.sinaimg.cn/mw690/001B8XzRgy6NAeYnH087c&690'
	c = ImageInfoFormat(u)
	c.start()
	print c.pic_info
