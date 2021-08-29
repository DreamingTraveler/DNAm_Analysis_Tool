import sys
import os
import io
import urllib
import config
import util
import base64
import pandas as pd
import matplotlib.pyplot as plt
import rpy2.robjects as ro
import PIL.Image as Image
from rpy2.robjects.packages import importr
from rpy2.robjects import r, pandas2ri
from rpy2.robjects.conversion import localconverter
from flask import Blueprint, request, abort, render_template, redirect, \
 url_for, current_app, make_response, send_file
from flask.views import MethodView
# from bioinfokit import analys, visuz



blueprint = Blueprint('main', __name__)
dmp_tables = util.DMPTables()

class DMP():
    def __init__(self, dmp):
        self.probe_id = dmp[0]
        self.logFC = '{:.5}'.format(dmp[1])
        self.t_val = '{:.5}'.format(dmp[2])
        self.p_val = '{:.2e}'.format(dmp[3])
        self.chr = dmp[4]
        self.coord = dmp[5]
        self.gene = dmp[6]
        self.feat_cgi = dmp[7]

class MainView(MethodView):
    def get(self):
        _, filter_dmp_df, dmp_class_list = self.get_data_from_csv()
        page, max_dmp_num, dmp_per_page, total_page = self.get_page_info(dmp_class_list)
        dmp_class_sublist = self.get_dmp_list_for_target_page(page, max_dmp_num, dmp_per_page, dmp_class_list)
        
        return render_template('base/index.html', dmp_list=dmp_class_sublist, 
            page=page, total_page=total_page, probe_num=len(dmp_class_list), 
            gene_num=filter_dmp_df["gene"].nunique())

    def post(self):
        _, filter_dmp_df, dmp_class_list = self.get_data_from_csv()
        page, max_dmp_num, dmp_per_page, total_page = self.get_page_info(dmp_class_list)
        dmp_class_sublist = self.get_dmp_list_for_target_page(page, max_dmp_num, dmp_per_page, dmp_class_list)
        probe_num = len(dmp_class_list)
        gene_num = filter_dmp_df["gene"].nunique()

        return render_template('base/dmp_table.html', dmp_list=dmp_class_sublist, 
            page=page, total_page=total_page, probe_num=probe_num,
            gene_num=gene_num)

    def get_df_on_conditions(self):
        input_csv = ""
        df = None
        cancer_type = request.cookies.get('cancerType')
        race = request.cookies.get('raceOption')
        stage = request.cookies.get('stageOption')

        if cancer_type == "bladder":
            df = dmp_tables.bladder_dmp_df

            if race is not None:
                if race == "asian":
                    df = dmp_tables.bladder_asian_dmp_df
                elif race == "white":
                    df = dmp_tables.bladder_white_dmp_df
                elif race == "black":
                    df = dmp_tables.bladder_black_dmp_df

            if stage is not None:
                if stage == "early":
                    df = dmp_tables.bladder_early_stage_dmp_df
                elif stage == "late":
                    df = dmp_tables.bladder_late_stage_dmp_df

        else:
            df = dmp_tables.colorectal_dmp_df

            if race is not None:
                if race == "asian":
                    df = dmp_tables.colorectal_asian_dmp_df
                elif race == "white":
                    df = dmp_tables.colorectal_white_dmp_df
                elif race == "black":
                    df = dmp_tables.colorectal_black_dmp_df

            if stage is not None:
                if stage == "early":
                    df = dmp_tables.colorectal_early_stage_dmp_df
                elif stage == "late":
                    df = dmp_tables.colorectal_late_stage_dmp_df

        return df

    def get_filter_dmp(self, df):
        filter_text = request.cookies.get('searchFilterText')
        filter_opt = request.cookies.get('searchFilterOption')
        logFC_threshold = request.cookies.get('logFCThreshold')
        is_hyper = request.cookies.get('isHyper')
        is_hypo = request.cookies.get('isHypo')
        rem_duplicate_genes = request.cookies.get('isDuplicateGenes')

        filter_text_list = []

        if logFC_threshold == None:
            logFC_threshold = 0.0
        else:
            logFC_threshold = float(logFC_threshold)


        # filter by logFC threshold
        df = df[df["logFC"].abs() >= logFC_threshold]

        # filter by methylation status
        if is_hyper == "false" and is_hypo == "false":
            df = df.iloc[0:0]
        elif is_hyper == "false":
            df = df[df["logFC"] < 0]
        elif is_hypo == "false":
            df = df[df["logFC"] >= 0]

        # remove duplicate genes
        if rem_duplicate_genes == "true":
            df = df.sort_values(by="logFC", ascending=False, key=abs)
            df = df.drop_duplicates(subset=["gene"])
            df = df[df.gene != ""]

        if not filter_text:
            return df
        else:
            filter_text_list = filter_text.split("%2C")

        if filter_opt == "probe":
            return df[df["Probe_ID"].str.contains('|'.join(filter_text_list))]

        elif filter_opt == "gene":
            # return df[df["gene"].str.contains('|'.join(filter_text_list), na=False)]
            return df[df["gene"].isin(filter_text_list)]

        return df

    def get_data_from_csv(self):
        df = self.get_df_on_conditions()
        df = df.fillna("")
        sub_df = df[config.SUB_DF_COLUMNS]
        filter_df = self.get_filter_dmp(sub_df)
        dmp_list = filter_df.values
        dmp_class_list = []
        
        for dmp in dmp_list:
            dmp_class = DMP(dmp)
            dmp_class_list.append(dmp_class)

        return sub_df, filter_df, dmp_class_list

    def get_page_info(self, dmp_class_list):
        page = request.cookies.get('page') # get the current page number from cookie
        if page == None:
            page = 1
        page = int(page)
        
        max_dmp_num = len(dmp_class_list)
        dmp_per_page = 10
        total_page = int((max_dmp_num-1) / dmp_per_page) + 1
        
        return page, max_dmp_num, dmp_per_page, total_page

    def get_dmp_list_for_target_page(self, page, max_dmp_num, dmp_per_page, dmp_class_list):
        dmp_idx_begin = (page-1)*dmp_per_page
        dmp_idx_end = page*dmp_per_page
        if dmp_idx_end >= max_dmp_num:
            dmp_idx_end = max_dmp_num+1

        dmp_class_sublist = dmp_class_list[dmp_idx_begin:dmp_idx_end]

        return dmp_class_sublist

class SaveDMPView(MainView):
    def post(self):
        file_type = request.form["fileType"]
        intersect_df = request.form["df"]

        _, filter_df, dmp_class_list = super(SaveDMPView, self).get_data_from_csv()
        cancer_type = request.cookies.get('cancerType')
        race = request.cookies.get('raceOption')
        stage = request.cookies.get('stageOption')
        logFC_threshold = request.cookies.get('logFCThreshold')

        cancer_type = cancer_type if cancer_type else "colorectal"
        race = race+"_" if race else ""
        stage = stage+"_" if stage else ""
        logFC_threshold = logFC_threshold if logFC_threshold else "0.0"

        filename = cancer_type + "_" + race + stage + "biomarkers_threshold_" + \
                    logFC_threshold

        result_df = filter_df
        if intersect_df:
            string_df = io.StringIO(intersect_df)
            result_df = pd.read_csv(string_df,
                sep=r"\s+", escapechar='\\', engine='python')
            print(result_df)

        if file_type == "xlsx":
            out = io.BytesIO()
            writer = pd.ExcelWriter(out, engine='xlsxwriter')
            result_df.to_excel(excel_writer=writer, index=False, encoding="utf-8")
            writer.save()
            # writer.close()

            content_disp = "attachment; filename={filename}.xlsx".format(filename=filename)
            resp = make_response(out.getvalue())
            resp.headers["Content-Disposition"] = content_disp
            resp.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        else: 
            content_disp = "attachment; filename={filename}.csv".format(filename=filename)
            resp = make_response(result_df.to_csv(index=False, encoding="utf-8"))
            resp.headers["Content-Disposition"] = content_disp
            resp.headers["Content-Type"] = "text/csv"
        
        resp.headers["Set-Cookie"] = "fileDownload=true; path=/"

        return resp

class PlotView(MainView):
    def post(self):
        plot_opt = request.cookies.get('plotOption')
        if not plot_opt or plot_opt != "volcano":
            return render_template("base/plots.html")  

        ori_df, filter_df, dmp_class_list = super(PlotView, self).get_data_from_csv()
        logFC_threshold = request.cookies.get('logFCThreshold')

        if logFC_threshold == None:
            logFC_threshold = 0.0
        else:
            logFC_threshold = float(logFC_threshold)
            if logFC_threshold == 0.0:
                logFC_threshold = 0.5
        
        with localconverter(ro.default_converter + pandas2ri.converter):
            r_dataframe = ro.conversion.py2rpy(ori_df)

        r['source']('./voc_plot.R')
        res_byte_array = r('generateVocPlot')(r_dataframe, logFC_threshold, 0.01)

        res = io.BytesIO(bytes(res_byte_array))
        res.seek(0)

        plot_url = base64.b64encode(res.getvalue()).decode()
        content = '<img src="data:image/png;base64,{}">'.format(plot_url)
       
        return render_template("base/plots.html", img_url=plot_url)                       

blueprint.add_url_rule('/', view_func=MainView.as_view(MainView.__name__))
blueprint.add_url_rule('/plot', view_func=PlotView.as_view(PlotView.__name__))
blueprint.add_url_rule('/save', view_func=SaveDMPView.as_view(SaveDMPView.__name__))