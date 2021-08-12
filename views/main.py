import sys
import os
import config
import pandas as pd
from flask import Blueprint, request, abort, render_template, redirect, url_for, current_app
from flask.views import MethodView


blueprint = Blueprint('main', __name__)

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

def get_data_from_csv():
    df = pd.read_csv(config.COLORECTAL_DMP_CSV)
    sub_df = df[config.SUB_DF_COLUMNS]
    dmp_list = sub_df.values
    dmp_class_list = []

    for dmp in dmp_list:
        dmp_class = DMP(dmp)
        dmp_class_list.append(dmp_class)

    return dmp_class_list

class MainView(MethodView):
    def get(self):
        dmp_class_list = get_data_from_csv()

        page = request.cookies.get('page') # get the current page number from cookie
        if page == None:
            page = 1
        page = int(page)
        
        max_dmp_num = len(dmp_class_list)
        dmp_per_page = 10
        total_page = int(max_dmp_num / dmp_per_page) + 1
        dmp_idx_begin = (page-1)*dmp_per_page
        dmp_idx_end = page*dmp_per_page
        if dmp_idx_end >= max_dmp_num:
            dmp_idx_end = max_dmp_num+1
        
        dmp_class_sublist = dmp_class_list[dmp_idx_begin:dmp_idx_end]
        
        return render_template('base/index.html', dmp_list=dmp_class_sublist, 
            page=page, total_page=total_page)

    # def post(self):
    #     dmp_class_list = get_data_from_csv()
        
    #     max_dmp_num = len(dmp_class_list)
    #     page = request.form["page"] 
    #     page = 1 if page == None else int(page)
        

    #     dmp_per_page = 10
    #     total_page = int(max_dmp_num / dmp_per_page) + 1
    #     dmp_idx_begin = (page-1)*dmp_per_page
    #     dmp_idx_end = page*dmp_per_page
    #     if dmp_idx_end >= max_dmp_num:
    #         dmp_idx_end = max_dmp_num+1
        
    #     dmp_class_sublist = dmp_class_list[dmp_idx_begin:dmp_idx_end]

    #     return render_template('base/index.html', dmp_list=dmp_class_sublist, 
    #         page=page, total_page=total_page)
    



blueprint.add_url_rule('/', view_func=MainView.as_view(MainView.__name__))
