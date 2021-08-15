import sys
import os
import config
import util
import pandas as pd
from flask import Blueprint, request, abort, render_template, redirect, url_for, current_app
from flask.views import MethodView


blueprint = Blueprint('main', __name__)
dmp_tables = util.DMPTables()

class DMP():
    def __init__(self, dmp):
        self.probe_id = dmp[0]
        self.logFC = dmp[1]
        self.t_val = dmp[2]
        self.p_val = '{:.2e}'.format(dmp[3])
        self.chr = dmp[4]
        self.coord = dmp[5]
        self.gene = dmp[6]
        self.feat_cgi = dmp[7]

class MainView(MethodView):
    def get(self):
        filter_dmp_df, dmp_class_list = self.get_data_from_csv()
        page, max_dmp_num, dmp_per_page, total_page = self.get_page_info(dmp_class_list)
        dmp_class_sublist = self.get_dmp_list_for_target_page(page, max_dmp_num, dmp_per_page, dmp_class_list)
        
        return render_template('base/index.html', dmp_list=dmp_class_sublist, 
            page=page, total_page=total_page, probe_num=len(dmp_class_list), 
            gene_num=filter_dmp_df["gene"].nunique())

    def post(self):
        filter_dmp_df, dmp_class_list = self.get_data_from_csv()
        page, max_dmp_num, dmp_per_page, total_page = self.get_page_info(dmp_class_list)
        dmp_class_sublist = self.get_dmp_list_for_target_page(page, max_dmp_num, dmp_per_page, dmp_class_list)
        probe_num = len(dmp_class_list)
        gene_num = filter_dmp_df["gene"].nunique()

        return render_template('base/dmp_table.html', dmp_list=dmp_class_sublist, 
            page=page, total_page=total_page, probe_num=probe_num,
            gene_num=gene_num)

    def get_df_by_cancer_type(self):
        input_csv = ""
        df = None
        cancer_type = request.cookies.get('cancerType')
        if cancer_type == "bladder":
            df = dmp_tables.bladder_dmp_df
        else:
            df = dmp_tables.colorectal_dmp_df

        return df

    def get_filter_dmp(self, df):
        filter_text = request.cookies.get('searchFilterText')
        filter_opt = request.cookies.get('searchFilterOption')
        logFC_threshold = request.cookies.get('logFCThreshold')
        is_hyper = request.cookies.get('isHyper')
        is_hypo = request.cookies.get('isHypo')

        if logFC_threshold == None:
            logFC_threshold = 0.0
        else:
            logFC_threshold = float(logFC_threshold)

        if filter_text == "" or filter_text == " ":
            return df

        if filter_opt == "probe":
            return df[df["Probe_ID"].str.contains(filter_text)]
        elif filter_opt == "gene":

            return df[df["gene"].str.contains(filter_text, na=False)]

        # filter by logFC threshold
        df = df[df["logFC"].abs() >= logFC_threshold]

        # filter by methylation status
        if is_hyper == "false" and is_hypo == "false":
            df = df.iloc[0:0]
        elif is_hyper == "false":
            df = df[df["logFC"] < 0]
        elif is_hypo == "false":
            df = df[df["logFC"] >= 0]


        return df

    def get_data_from_csv(self):
        df = self.get_df_by_cancer_type()
        df = df.fillna("")
        sub_df = df[config.SUB_DF_COLUMNS]
        filter_df = self.get_filter_dmp(sub_df)
        dmp_list = filter_df.values
        dmp_class_list = []
        
        for dmp in dmp_list:
            dmp_class = DMP(dmp)
            dmp_class_list.append(dmp_class)

        return filter_df, dmp_class_list

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
        

blueprint.add_url_rule('/', view_func=MainView.as_view(MainView.__name__))
