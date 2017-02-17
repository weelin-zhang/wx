#encoding=utf8
from bs4 import BeautifulSoup
import urllib2
import logging

def get_music(musicname,sr=None):
    try:
        url = 'http://www.xiami.com/search?key={music_name}'.format(music_name=musicname)
        request = urllib2.Request(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'})
        html = urllib2.urlopen(request).read()
        soup = BeautifulSoup(html,'lxml')
        #soup = BeautifulSoup(html,'html.parser')
        song_tag_l =  soup.tbody.find_all('tr')
	print len(song_tag_l)
	song_info_l=[]
	for song_tag in song_tag_l:
        	name = song_tag.find_all('td')[1].a['title']
        	url = song_tag.find_all('td')[1].a['href']
		songer = song_tag.find_all('td')[2].a.get_text()
        	decription = song_tag.find_all('td')[3].a.get_text()
		#print 'url:',url,'songer:',songer,decription
		if not sr:
			return (name,url,songer.strip(),decription.strip())
		if songer.find(sr.decode('utf-8'))!=-1:
			#print name,url,songer,decription
			#print songer.strip()
			return (name,url,songer.strip(),decription.strip())
		song_info_l.append((name,url,songer.strip(),decription.strip()))
	return song_info_l[0]
	
    except Exception as e:
	#logger.error(e)
	print e
        return None


if __name__ == '__main__':
    print get_music('爱')

