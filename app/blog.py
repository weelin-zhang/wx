#encoding=utf8
from flask import Blueprint,render_template, request,redirect,url_for,g
from flask_login import login_required,logout_user,current_user
from plugs import blog_info
blog = Blueprint('blog',__name__)


@blog.before_request
def before_request():  
    g.user = current_user  

@blog.route('/index/')
@blog.route('/')
@login_required
def index():
    
    blog_list =blog_info.get_blog_info() 
    return render_template('blog/index.html',blogs=blog_list,user=g.user)



@blog.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'),user=g.user)
