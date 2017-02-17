# encoding=utf8
import time
import json
import os
import sys
import requests
from bs4 import BeautifulSoup
record_d = {}
#tianqi_record_path = 'citys_info'
tianqi_record_path = os.path.join(os.path.dirname(__file__),'citys_info')
WINDOWS = os.name == 'nt'

def save_info(record_d, path):
    with open(path, 'w') as f:
        json.dump(record_d,f)

def get_info_from_file(path):
    if not os.path.exists(path):
        return None
    with open(path,'r') as f:
        return json.load(f)
def get_provinces_info():
    #爬取所有省市自治区[(city,url)...]
    baseurl = 'http://tianqi.2345.com/'
    html  = requests.get(baseurl).text
    soup = BeautifulSoup(html)
    citys_name_l = list(a.getText() for a in soup.find('div',class_='clearfix custom').findAll('a'))
    citys_link_l = list('tianqi.2345.com'+a['href'] for a in soup.find('div',class_='clearfix custom').findAll('a'))
    result_l = list(zip(citys_name_l,citys_link_l))
    #[('beijing',url),......,]
    return result_l
def get_citys_info(province_l):
    global record_d
    # Session = Session_class()
    ProvinceName = slice(0,1)
    ProvinceUrl = slice(1,2)
    for p in province_l:
        url='http://'+p[ProvinceUrl][0]
        html =  requests.get(url).text
        s = BeautifulSoup(html)
        dds = s.find('div',{'class':'citychk'}).find_all('dd')
        for d in dds:
            tmp_l = d.find_all('a')
            for city in tmp_l:
                record_d[city.getText().strip()] = 'http://tianqi.2345.com'+city['href']
            save_info(record_d,tianqi_record_path)

def create_city_info():
    province_l = get_provinces_info()
    get_citys_info(province_l)



def get_weather_info(city):
    record = get_info_from_file(tianqi_record_path)
    #print record.keys()
    if city not in record.keys():
	#print type(city)
        return None
    r = requests.get(record[city])
    soup = BeautifulSoup(r.text)
    days= soup.find('div',id='day7info').find_all('li')
	
    weather_info=[]
    for day in days:
	info_1 = day.p.get_text().strip()+'\n'
	info_2 = day.b.get_text().strip()+'\n'
	info_3 = day.i.get_text().strip()+'\n'
	weather_info.append(info_1+info_2+info_3)
		
        #print('-'*20)

    return ''.join(weather_info)
    #print ''.join(weather_info)
		

		
		

def main():
    d = get_info_from_file(tianqi_record_path)
    if not d:
        print('no record...')
        try:
            print('create record...')
            create_city_info()
        except Exception as e:
            print(e)
        finally:
            d = get_info_from_file(tianqi_record_path)
    if not d:
        sys.exit(u'获取信息失败,out')


    while True:
        if sys.version_info<(3,2):
            city = raw_input('Input the city to get weather(quit/out):')
            if WINDOWS:
                city = city.decode('gbk')
            else:
                city = city.decode('utf-8')
        else:
            city = input('Input the city to get weather(quit/out):')
        if city.lower() == 'quit' or city.lower() == 'out':
            sys.exit('bye..')
        if city in d.keys():
            #get_weather_info(city,d[city])
            get_weather_info(city)
        else:
            print(u'请输入正确的城市')
        continue

if __name__ == '__main__':
    main()
