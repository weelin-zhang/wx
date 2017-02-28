#encoding=utf8
import json
from app import db
from flask import Blueprint,render_template, request,redirect,url_for,flash,Markup,g
from flask_login import login_required, login_user,logout_user,current_user
from models import User,DepartmentType,Solution
from .plugs import weather as wh
admin = Blueprint('admin',__name__)


@admin.before_request  
def before_request():  
    g.user = current_user 

@admin.route('/')
@login_required
def index():
    user = g.user
    return render_template('admin/index.html',user=user)

@admin.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method=='POST':  
        username, pwd = request.form.get('username',None), request.form.get('password',None)
        user = User.query.filter_by(username=username,password=pwd).first()
        if not user:
            flash(u'用户名密码不正确')
            return render_template('admin/login.html')
        login_user(user)
	return redirect(request.args.get('next') or url_for('admin.index'))
    return render_template('admin/login.html',message='')
@admin.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))


@admin.route('/depart/',methods=['POST','GET'])
@login_required
def depart():
    user = g.user
    if request.method != 'POST':
        return render_template('admin/depart.html',title='Department Manager',user=user)
    
    p_departname = request.form.get('departtype',None)
    if not p_departname:
	return Markup('<p>no input,%s</p>'%('<a style="text-decoration:none;font-size:20px;" href="/admin/depart/">Click Back</a>'))
    fac_obj = DepartmentType(departname=p_departname)
    db.session.add(fac_obj)
    db.session.commit()
    flash(u'添加成功')
    return render_template('admin/depart.html',title='Department Manager',user=user)

@admin.route('/addsolution/',methods=['POST','GET'])
@login_required
def add():
    user = g.user
    factories = DepartmentType.query.all()
    if request.method != 'POST':
        return render_template('admin/addsolution.html',title='Add Solution',factories=factories,user=user)
    
    p_factory_id = request.form.get('select_factory',None)
    #print p_factory_id
    if not int(p_factory_id):
	flash(u'请选择设备供应商')
    	return render_template('admin/addsolution.html',title='Add Solution',factories=factories,user=user)
    p_troublename = request.form.get('p_troublename',None)
    p_solution = request.form.get('p_solution',None)
    if p_troublename == 'describe trouble' or p_solution == 'make solution':
	flash(u'请输入有效内容')
    solution_obj = Solution(troublename=p_troublename,solution=p_solution,type_id=p_factory_id)
    db.session.add(solution_obj)
    db.session.commit()
    flash(u'添加成功')
    return render_template('admin/addsolution.html',title='Add Solution',factories=factories,user=user) 
   
@admin.route('/editsolution/<int:solution_id>/')
@login_required
def edit(solution_id):
    user = g.user
    obj = Solution.query.filter_by(id=int(solution_id)).first()
    return render_template('admin/editsolution.html',title="Update Solution",Solution=obj,user=user)



@admin.route('/updatesolution/<int:solution_id>/',methods=['POST'])
@login_required
def update(solution_id):
    user = g.user
    p_troublename = request.form.get('p_troublename',None)
    p_solution = request.form.get('p_solution',None)
    if not p_troublename or not p_solution:
        return u'更新失败'
    obj = Solution.query.filter_by(id=int(solution_id)).first()
    obj.troublename, obj.solution = p_troublename, p_solution
    db.session.commit()
    return redirect(url_for('admin.show'))

@admin.route('/deletesolution/<int:solution_id>/')
@login_required
def delete(solution_id):
    user = g.user
    obj = Solution.query.filter_by(id=int(solution_id)).first()
    db.session.delete(obj)
    db.session.commit()
    return redirect(url_for('admin.show'))


@admin.route('/showsolution/')
@login_required
def show():
    user = g.user
    record_is_exists = False
    data_l = []
    solution_d={}
    departs = DepartmentType.query.all()
    for styleindex,depart in enumerate(departs,1):
        record_is_exists = record_is_exists or len(depart.solutions)>0 
        solution_d = {}
        solution_d['departname'] = depart.departname
        solution_d['solutions'] = depart.solutions
        solution_d['style'] = 'style_'+str(styleindex)
        data_l.append(solution_d)
    #print record_is_exists
    return render_template('admin/showsolution.html',title="Show Solutions",datas=data_l,record=record_is_exists,user=user)

@admin.route('/weather/',methods=['POST'])
#@login_required
def weather():
    city = request.form.get('cur_city')
    #print 'ddd',city
    info = wh.get_weather_info(city)
    d_d = {'info': info}
    return json.dumps(d_d)
    
