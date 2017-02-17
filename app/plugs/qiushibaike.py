from bs4 import BeautifulSoup
import requests
import random

def get5infos():
	randindex = random.randint(1,10)
	url='http://www.qiushibaike.com/hot/page/%s'%(randindex)
	r=requests.get(url)
	soup = BeautifulSoup(r.text)
	ll = []
	for i in soup.find_all('div',class_='article block untagged mb15'):
    		humor = i.find('span').get_text()
    		if len(humor)>25:
			ll.append(i.find('span').get_text())
	INDEX = random.randint(2,8)
	tmp_l = []
	for index,i in enumerate(ll[0:INDEX],1):
		tmp_l.append(str(index)+'.'+i+'\n'+'------------------')	
	

	return tmp_l

if __name__=='__main__':
	print '\n'.join(get5infos())
