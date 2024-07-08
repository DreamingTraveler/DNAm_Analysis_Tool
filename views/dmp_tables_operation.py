import os
import io
import pandas as pd
import config
import util
import json
from flask import Blueprint, request, abort, render_template, redirect, \
 url_for, current_app, make_response, send_file, flash
from flask.views import MethodView
from werkzeug.utils import secure_filename

blueprint = Blueprint('dmp_tables_operation', __name__)
dmp_tables = util.DMPTables()
pd.options.display.max_columns = 16384
pd.options.display.max_rows = 1048576
pd.set_option('display.expand_frame_repr', False)

class DMPTablesOPView(MethodView):
	def get(self):
		return render_template("dmp_tables_operation/dmp_tables_operation.html")

class UploadfileView(MethodView):
	def get(self):
		return render_template("dmp_tables_operation/dmp_tables_operation.html")
	def post(self):
		uploaded_files = request.files
		df_list = []
		# if uploaded_file.filename == '':
		# 	flash('No selected file')
		# 	return redirect(request.url)

		for f in uploaded_files:
			file = uploaded_files.get(f)
			if not self.allowed_file(file.filename):
				flash('File type error (.xlsx and .csv only)')
				return render_template("dmp_tables_operation/dmp_tables_operation.html")

			if file and self.allowed_file(file.filename):
				safe_filename = secure_filename(file.filename)
				# file.save(os.path.join(config.UPLOAD_FOLDER, safe_filename))
				file_type = file.filename.split(".")[-1]
				if file_type == "csv":
					df = pd.read_csv(file)
				else:
					df = pd.read_excel(file)
				df_list.append(df)
		
		target_df = self.operate_files(df_list)
		target_df = target_df.fillna("NA")
		headers = list(target_df.columns)
		result_list = target_df.values.tolist()
		row_num = len(result_list)

		return render_template("dmp_tables_operation/preview_table.html", 
			target_df=target_df,
			headers=headers, result=result_list, row_num=row_num)

	def allowed_file(self, filename):
		return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

	def operate_files(self, df_list):
		op_target = request.cookies.get("operatedTarget")
		operation = request.cookies.get("operation")

		if request.cookies.get("operatedTarget") == "probe":
			op_target = "Probe_ID"
		else:
			op_target = "gene"

		
		# target_df = df_list[0][op_target] if operation == "intersection" \
		# 						else df_list[0]

		target_df = df_list[0]
		
		concat_df = None

		for df in df_list[1:]:
			if operation == "intersection":
				target_df = pd.merge(target_df, df, how="inner", on=[op_target])
			elif operation == "left":
				target_df = pd.merge(target_df, df, how="left", on=[op_target])
			else: # symmetric diff
				target_df = pd.concat([target_df, df])
		
		if operation == "symmetricDiff":
			target_df = target_df.drop_duplicates(subset=op_target, keep=False)
			
		return target_df		

blueprint.add_url_rule('/', 
	view_func=DMPTablesOPView.as_view(DMPTablesOPView.__name__))
blueprint.add_url_rule('/upload', 
	view_func=UploadfileView.as_view(UploadfileView.__name__))