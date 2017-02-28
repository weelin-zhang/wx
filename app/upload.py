#encoding=utf8
import os,sys
from flask import Blueprint, request, render_template, send_from_directory, g, url_for, flash,redirect,make_response,send_file
from flask_login import login_required,login_user,current_user
from werkzeug.utils import secure_filename
from app import app

upload = Blueprint('upload',__name__)

#检查上传文件类型是否符合要求
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@upload.before_request
def before_request():
    g.user = current_user

@upload.route('/')
@upload.route('/up/',methods=['POST','GET'])
@login_required
def upload_file():
    if request.method == 'POST':
        f_handler = request.files.get('upload_file')
        fname = secure_filename(f_handler.filename)  # 获取一个安全的文件名，且仅仅支持ascii字(也就是源文件名)
        if not allowed_file(fname):
	    flash(u'文件格式不对or没有选择文件')
            return render_template('upload/upload.html', uploadtypes=app.config['ALLOWED_EXTENSIONS'])
            #return render_template('upload/upload.html', status='文件格式不对', uploadtypes=app.config['ALLOWED_EXTENSIONS'])
        f_handler.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
        flash(u'上传成功')
        return redirect(url_for('upload.upload_file'))
        return render_template('upload/upload.html', status='upload success')
    return render_template('upload/upload.html', title='UploadPage', uploadtypes=app.config['ALLOWED_EXTENSIONS'])


@upload.route('/index/')
def index():
   files_l = os.listdir('/home/weelin/python/my_envs/wx/app/upload/') 
   return render_template('upload/download.html',files = files_l)

@upload.route('/download/<filename>')
#@login_required
def download(filename):
    #print app.config['UPLOAD_FOLDER'],filename
    #return send_from_directory(app.config['UPLOAD_FOLDER'],filename)
    print os.path.join(app.config['UPLOAD_FOLDER'],filename)
    response = make_response(send_file('upload'+'/'+filename))
    response.headers['Content-Disposition'] = 'attachment; filename={};'.format(filename)
    return response

