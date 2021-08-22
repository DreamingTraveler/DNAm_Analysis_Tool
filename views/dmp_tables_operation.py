import os
import pandas as pd
import config
import util
from flask import Blueprint, request, abort, render_template, redirect, \
 url_for, current_app, make_response, send_file, flash
from flask.views import MethodView
from werkzeug.utils import secure_filename

blueprint = Blueprint('dmp_tables_operation', __name__)
dmp_tables = util.DMPTables()


class DMPTablesOPView(MethodView):
	def get(self):
		return render_template("dmp_tables_operation/dmp_tables_operation.html")

class UploadfileView(MethodView):
	def post(self):
		uploaded_file = request.files["file"]
		# if uploaded_file.filename == '':
		# 	flash('No selected file')
		# 	return redirect(request.url)

		if not self.allowed_file(uploaded_file.filename):
			flash('File type error (.xlsx and .csv only)')
			print("SS")
			return render_template("dmp_tables_operation/dmp_tables_operation.html")

		if uploaded_file and self.allowed_file(uploaded_file.filename):
			safe_filename = secure_filename(uploaded_file.filename)
			uploaded_file.save(os.path.join(config.UPLOAD_FOLDER, safe_filename))

		# print(uploaded_file.filename)
		return redirect(url_for('dmp_tables_operation.DMPTablesOPView'))
	def allowed_file(self, filename):
		return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


blueprint.add_url_rule('/', 
	view_func=DMPTablesOPView.as_view(DMPTablesOPView.__name__))
blueprint.add_url_rule('/upload', 
	view_func=UploadfileView.as_view(UploadfileView.__name__))