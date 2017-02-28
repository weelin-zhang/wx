#encoding=utf8
import requests
import re
import sys
import json
#reload(sys)
#sys.setdefaultencoding('utf-8')
PAGE_NUM = 2

base_url = 'http://www.cnblogs.com/diaosir/default.html?page='
title_regex = re.compile(r'<div class="postTitle">.*?>(.*?)</a>',re.S)
url_regex = re.compile(r'<div class="postTitle">.*?<a id="homepage.*?href="(.*?)".*?</a>',re.S)
post_regex = re.compile(r'<div class="postDesc">(.*?)<a.*')
read_count_regex = re.compile(r'.*?\((\d*).')

def get_blog_info():
        print 'once'
        titles_l,urls_l = [],[]
        for i in range(PAGE_NUM):
            tmp_titles_l,tmp_urls_l = [],[]
            url = base_url+'%s'%(int(i)+1)
            r = requests.get(url)
            html = r.content
            tmp_titles_l = re.findall(title_regex,html)
            tmp_urls_l = re.findall(url_regex,html)
            titles_l.extend(tmp_titles_l)
            urls_l.extend(tmp_urls_l)
        
        d_l=[]
	for info in zip(titles_l,urls_l):
	    tmp_d = {}
	    tmp_d['title'],tmp_d['url'] = info[0],info[1]
	    d_l.append(tmp_d)
        return d_l



if __name__=='__main__':
    result = get_blog_info()
    print result[0]
