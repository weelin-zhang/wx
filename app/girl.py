#encoding=utf8
from flask import Blueprint,render_template, request,redirect,url_for,g
from flask_login import login_required,logout_user,current_user
girl = Blueprint('girl',__name__)


@girl.before_request
def before_request():  
    g.user = current_user  

@girl.route('/index/')
@girl.route('/')
@login_required
def index():
    if current_user.username != 'zhangweijian':
        return render_template('girl/403.html',user=g.user),403
    return render_template('girl/index.html',user=g.user)


@girl.route('/selfcheck/')
def check():
    return render_template('girl/selfcheck.html',title="For Love")


@girl.route('/d3/')
@login_required
def d3():
    #return 'shoufengqin'
    return render_template('girl/3d_dongtai.html',user=g.user)

@girl.route('/shoufengqin1/')
@login_required
def shoufengqin():
    #return 'shoufengqin'
    return render_template('girl/shoufengqin/shoufengqin.html',user=g.user)



@girl.route('/shoufengqin2/')
@login_required
def shoufengqindemo():
    return render_template('girl/shoufengqin/demo.html',user=g.user)

@girl.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'),user=g.user)
