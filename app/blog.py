#encoding=utf8
import json
import os
from flask import Blueprint,render_template, request,redirect,url_for,g
from flask_login import login_required,logout_user,current_user
from plugs import blog_info
blog = Blueprint('blog',__name__)
BLOG_INFO = []
@blog.before_request
def before_request():  
    g.user = current_user  

@blog.route('/index/')
@blog.route('/')
@login_required
def index():
    global BLOG_INFO
    if not BLOG_INFO:
    	BLOG_INFO = blog_info.get_blog_info()
    return render_template('blog/index.html',blogs=BLOG_INFO,user=g.user)





@blog.route('/chart/',methods=['POST'])
@login_required
def chart():
    if request.method == 'POST':
        info = blog_info.get_blogchart_info()
        blog_title, blog_lengend, blog_xaxis = '访问量',['访问量'],info[0]
        blog_series = {'name': '访问量',
                       'type': 'bar',
                       'data': info[1]
                       }
        d_dict = {'title': blog_title,'legend': blog_lengend, 'xAxis': blog_xaxis, 'series': blog_series}
    return json.dumps(d_dict)


