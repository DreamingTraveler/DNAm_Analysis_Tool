import sys
import os
import config
import pandas as pd
from flask import Blueprint, request, abort, render_template, redirect, url_for, current_app
from flask.views import MethodView


blueprint = Blueprint('main', __name__)

def get_csv_by_cancer_type():
    input_csv = ""
    cancer_type = request.cookies.get('cancerType')
    if cancer_type == "bladder":
        input_csv = config.BLADDER_DMP_CSV
    else:
        input_csv = config.COLORECTAL_DMP_CSV

    return input_csv

def get_filter_dmp(df):
    filter_text = request.cookies.get('searchFilterText')
    filter_opt = request.cookies.get('searchFilterOption')

    if filter_text == "" or " ":
        return df

    if filter_opt == "probe":
        return df[df["Probe_ID"].str.contains(filter_text)]
    elif filter_opt == "gene":
        return df[df["gene"].str.contains(filter_text, na=False)]

    return df

def get_data_from_csv():
    input_csv = get_csv_by_cancer_type()
    df = pd.read_csv(input_csv)
    sub_df = df[config.SUB_DF_COLUMNS]
    filter_df = get_filter_dmp(sub_df)
    dmp_list = filter_df.values
    dmp_class_list = []

    for dmp in dmp_list:
        dmp_class = DMP(dmp)
        dmp_class_list.append(dmp_class)

    return dmp_class_list

def get_page_info(dmp_class_list):
    page = request.cookies.get('page') # get the current page number from cookie
    if page == None:
        page = 1
    page = int(page)
    
    max_dmp_num = len(dmp_class_list)
    dmp_per_page = 10
    total_page = int(max_dmp_num / dmp_per_page) + 1
    
    return page, max_dmp_num, dmp_per_page, total_page

def get_dmp_list_for_target_page(page, max_dmp_num, dmp_per_page, dmp_class_list):
    dmp_idx_begin = (page-1)*dmp_per_page
    dmp_idx_end = page*dmp_per_page
    if dmp_idx_end >= max_dmp_num:
        dmp_idx_end = max_dmp_num+1

    dmp_class_sublist = dmp_class_list[dmp_idx_begin:dmp_idx_end]

    return dmp_class_sublist

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
        dmp_class_list = get_data_from_csv()
        page, max_dmp_num, dmp_per_page, total_page = get_page_info(dmp_class_list)
        dmp_class_sublist = get_dmp_list_for_target_page(page, max_dmp_num, dmp_per_page, dmp_class_list)
        
        return render_template('base/index.html', dmp_list=dmp_class_sublist, 
            page=page, total_page=total_page)

    def post(self):
        dmp_class_list = get_data_from_csv()
        page, max_dmp_num, dmp_per_page, total_page = get_page_info(dmp_class_list)
        dmp_class_sublist = get_dmp_list_for_target_page(page, max_dmp_num, dmp_per_page, dmp_class_list)

        return render_template('base/dmp_table.html', dmp_list=dmp_class_sublist, 
            page=page, total_page=total_page)
    

blueprint.add_url_rule('/', view_func=MainView.as_view(MainView.__name__))
