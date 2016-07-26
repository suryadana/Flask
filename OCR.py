#!/usr/bin/env python
import os
import pwd
import grp
from PIL import Image
import pytesseract
from flask import *
from werkzeug import secure_filename

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
BASE_URL = 'http://localhost'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
	uid = pwd.getpwnam("pendekar_langit").pw_uid
	gid = grp.getgrnam("pendekar_langit").gr_gid
	if request.method == 'GET':
		content = {
			'title' : 'OCR',
			'base_url' : BASE_URL,
		}
		return render_template('template_index.html', content=content)
	elif request.method == 'POST':
		files = []
		target = os.path.join(APP_ROOT, 'uploads')
		print target
		if not os.path.isdir(target):
			os.mkdir(target, 0775)
			os.chown(target, uid, gid)

		for file in request.files.getlist("file"):
			print(file)
			filename = file.filename
			destination = "/".join([target, filename])
			print filename
			print destination
			file.save(destination)
			os.chown(destination, uid, gid)
			files.append(filename)
		return redirect(url_for('read_string', filename=files[0]))


@app.route('/read/<filename>')
def read_string(filename):
	print filename
	target = os.path.join(APP_ROOT, 'uploads')
	destination = "/".join([target, filename])
	result =  pytesseract.image_to_string(Image.open(destination), lang='ind')
	os.remove(destination)
	content = {
		'title' : 'OCR',
		'result' : result,
	}
	return render_template('template_read.html', content=content)

if __name__ == '__main__':
	app.run(port=80,debug=True)