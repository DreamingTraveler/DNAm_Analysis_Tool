import sys
import os
import io
import urllib
import config
import math
import util
import base64
import pandas as pd
import numpy as np
import PIL.Image as Image
# import rpy2.robjects as ro
# from rpy2.robjects import r, pandas2ri
# from rpy2.robjects.conversion import localconverter
from flask import Blueprint, request, abort, render_template, redirect, \
 url_for, current_app, make_response, send_file, jsonify, json
from flask.views import MethodView
# from bioinfokit import analys, visuz



blueprint = Blueprint('main', __name__)
dmp_tables = util.DMPTables()
biomarker_tables = util.BiomarkerTables()
validation_res_tables = util.ValidationResultTables()

class DMP():
    def __init__(self, dmp):
        self.probe_id = dmp[0]
        self.beta_diff = '{:.5}'.format(dmp[1])
        self.t_val = '{:.5}'.format(dmp[2])
        self.p_val = '{:.2e}'.format(dmp[3])
        self.chr = dmp[4]
        self.coord = dmp[5]
        self.gene = dmp[6]
        self.feat_cgi = dmp[7]

class Biomarker():
    def __init__(self, dmp):
        self.probe_id = dmp[0]
        self.beta_diff = '{:.5}'.format(dmp[1])
        self.t_val = '{:.5}'.format(dmp[2])
        self.p_val = '{:.2e}'.format(dmp[3])
        self.gene = dmp[4]
        self.feat_cgi = dmp[5]
        self.chr = dmp[6]
        self.coord = dmp[7]
        self.is_candidate = dmp[8]

class ValidationRes():
    def __init__(self, dmp):
        self.probe_id = dmp[0]
        self.gene = dmp[1]
        self.optimal_cut_point = dmp[2]
        if math.isnan(dmp[3]):
            self.accuracy = dmp[3]
        else:
            self.accuracy = '{:.4}'.format(dmp[3]*100) + ' %'

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

        elif cancer_type == "lung":
            df = dmp_tables.lung_dmp_df

        elif cancer_type == "liver":
            df = dmp_tables.liver_dmp_df

        elif cancer_type == "pancreas":
            df = dmp_tables.pancreas_dmp_df

        elif cancer_type == "prostate":
            df = dmp_tables.prostate_dmp_df

        elif cancer_type == "breast":
            df = dmp_tables.breast_dmp_df

        elif cancer_type == "ovarian":
            df = dmp_tables.ovarian_dmp_df

        elif cancer_type == "esophagus":
            df = dmp_tables.esophagus_dmp_df

        elif cancer_type == "stomach":
            df = dmp_tables.stomach_dmp_df

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
    def get(self):
        return render_template("base/plots.html") 

    def post(self):
        plot_opt = request.cookies.get('plotOption')
        logFC_threshold = request.cookies.get('logFCThreshold')

        if logFC_threshold == None:
            logFC_threshold = 0.0
        else:
            logFC_threshold = float(logFC_threshold)
            # if logFC_threshold == 0.0:
            #     logFC_threshold = 0.5  

        if plot_opt == "enrichedGenePlot":
            df = super(PlotView, self).get_df_on_conditions()
            enriched_genes_list = self.get_enriched_genes(df, logFC_threshold)

            return jsonify(enriched_genes_list)

        ori_df, filter_df, dmp_class_list = super(PlotView, self).get_data_from_csv()
        
        
        with localconverter(ro.default_converter + pandas2ri.converter):
            r_dataframe = ro.conversion.py2rpy(ori_df)

        r['source']('./voc_plot.R')
        res_byte_array = r('generateVocPlot')(r_dataframe, logFC_threshold, 0.01)

        res = io.BytesIO(bytes(res_byte_array))
        res.seek(0)

        plot_url = base64.b64encode(res.getvalue()).decode()
        content = '<img src="data:image/png;base64,{}">'.format(plot_url)
       
        return render_template("base/plots.html", img_url=plot_url)    

    def get_enriched_genes(self, df, logFC_threshold):
        df = df[df["gene"] != ""]
        df = df[df["logFC"].abs() >= logFC_threshold]
        df["pos_oder_neg"] = np.sign(df["logFC"]) # add a new column to designate the sign of logFC
        # gene_probe_num = df.groupby(["gene"]).size().reset_index(name="counts")
        # gene_probe_num = gene_probe_num.sort_values(by="counts", ascending=False)

        if df.empty == True:
            return []

        gene_probe_num = df.groupby("gene").pos_oder_neg.value_counts().unstack()
        gene_probe_num = gene_probe_num.fillna(0)
        gene_probe_num = gene_probe_num.astype('int64')
        gene_probe_num = gene_probe_num.reset_index()
        cols = list(gene_probe_num.columns)
        if -1.0 not in cols: # only hyper
            gene_probe_num[-1.0] = 0
        elif 1.0 not in cols:
            gene_probe_num[1.0] = 0
            
        gene_probe_num["counts"] = gene_probe_num.iloc[:, 1] + gene_probe_num.iloc[:, 2]
        gene_probe_num = gene_probe_num.sort_values(by="counts", ascending=False)
        gene_probe_num = gene_probe_num[["gene", -1.0, 1.0, "counts"]] # rearrange columns
        enriched_genes = gene_probe_num.iloc[:50] # return the top 50 enriched genes

        # 4 list included: gene, hypo_probe_count, hyper_probe_count, total_count
        enriched_genes_list = enriched_genes.values.T.tolist() 

        return enriched_genes_list

class PrimaryBiomarkersView(MainView):
    def get_df_on_conditions(self):
        input_csv = ""
        df = None
        cancer_type = request.cookies.get('cancerType')
        race = request.cookies.get('raceOption')
        stage = request.cookies.get('stageOption')

        if cancer_type == "bladder":
            pass
            # df = dmp_tables.bladder_dmp_df

            # if race is not None:
            #     if race == "asian":
            #         df = dmp_tables.bladder_asian_dmp_df
            #     elif race == "white":
            #         df = dmp_tables.bladder_white_dmp_df
            #     elif race == "black":
            #         df = dmp_tables.bladder_black_dmp_df

            # if stage is not None:
            #     if stage == "early":
            #         df = dmp_tables.bladder_early_stage_dmp_df
            #     elif stage == "late":
            #         df = dmp_tables.bladder_late_stage_dmp_df

        elif cancer_type == "colorectal":
            df = biomarker_tables.colorectal_primary_biomarker_df

        elif cancer_type == "lung":
            df = biomarker_tables.lung_primary_biomarker_df

        elif cancer_type == "liver":
            df = biomarker_tables.liver_primary_biomarker_df

        elif cancer_type == "pancreas":
            df = biomarker_tables.pancreas_primary_biomarker_df

        else:
            df = biomarker_tables.colorectal_primary_biomarker_df

        return df

    def get_filter_dmp(self, df):
        filter_text = request.cookies.get('searchFilterText')
        filter_opt = request.cookies.get('searchFilterOption')
        logFC_threshold = request.cookies.get('logFCThreshold')
        is_hyper = request.cookies.get('isHyper')
        is_hypo = request.cookies.get('isHypo')

        filter_text_list = []

        if logFC_threshold == None:
            logFC_threshold = 0.0
        else:
            logFC_threshold = float(logFC_threshold)

        # filter by methylation status
        if is_hyper == "false" and is_hypo == "false":
            df = df.iloc[0:0]
        elif is_hyper == "false":
            df = df[df["beta_diff"] < 0]
        elif is_hypo == "false":
            df = df[df["beta_diff"] >= 0]


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
        sub_df = df[config.PRIMARY_BIOMARKERS_COLUMNS]
        filter_df = self.get_filter_dmp(sub_df)
        biomarker_list = filter_df.values
        biomarker_class_list = []
        
        for biomarker in biomarker_list:
            biomarker_class_list.append(Biomarker(biomarker))

        # data for chromosome visualization
        vis_data = filter_df[["gene", "chr", "coord", "is_candidate"]]
        gene_list = []

        for idx, dmp in enumerate(vis_data.values):
            gene_name = dmp[0]
            chromosome = str(dmp[1])
            gene_coord = dmp[2]
            is_candidate = dmp[3]
            color = "#000000" # primary

            if is_candidate:
                color = "#800000"

            gene = {'name': gene_name, 'chr': chromosome, 'start': int(gene_coord), 'stop': int(gene_coord)+1,\
                    'color': color}
            gene_list.append(gene)


        return gene_list, filter_df, biomarker_class_list

    def get_box_plot_data(self, df):
        data_list = []
        Q1 = df.quantile(0.25, axis=1).values.tolist()
        Q3 = df.quantile(0.75, axis=1).values.tolist()
        max_val = df.max(axis=1).values.tolist()
        min_val = df.min(axis=1).values.tolist()
        median = df.median(axis=1).values.tolist()
        
        data_list.append(min_val)
        data_list.append(Q1)
        data_list.append(median)
        data_list.append(Q3)
        data_list.append(max_val)

        return np.array(data_list).transpose().tolist()
    def post(self):
        option = request.form["option"]

        if option != "":
            """
            box plot data: 2 * 252 * 5
            2: tumor, normal
            252: #primary biomarkers
            5: min, Q1, median, Q3, max
            """
            cancer_type = request.cookies.get('cancerType')

            normal_bd_df = biomarker_tables.colorectal_normal_beta_df
            tumor_bd_df = biomarker_tables.colorectal_tumor_beta_df

            if cancer_type == "lung":
                normal_bd_df = biomarker_tables.lung_normal_beta_df
                tumor_bd_df = biomarker_tables.lung_tumor_beta_df

            elif cancer_type == "liver":
                normal_bd_df = biomarker_tables.liver_normal_beta_df
                tumor_bd_df = biomarker_tables.liver_tumor_beta_df

            elif cancer_type == "pancreas":
                normal_bd_df = biomarker_tables.pancreas_normal_beta_df
                tumor_bd_df = biomarker_tables.pancreas_tumor_beta_df

            # elif cancer_type == "prostate":
            #     normal_bd_df = biomarker_tables.prostate_normal_beta_df
            #     tumor_bd_df = biomarker_tables.prostate_tumor_beta_df

            # elif cancer_type == "esophagus":
            #     normal_bd_df = biomarker_tables.esophagus_normal_beta_df
            #     tumor_bd_df = biomarker_tables.esophagus_tumor_beta_df
 

            normal_box_plot_data = self.get_box_plot_data(normal_bd_df)
            tumor_box_plot_data = self.get_box_plot_data(tumor_bd_df)
            box_plot_data = [normal_box_plot_data, tumor_box_plot_data]

            return jsonify(box_plot_data)

        else:
            vis_data, filter_biomarker_df, biomarker_class_list = self.get_data_from_csv()
            page, max_biomarker_num, biomarker_per_page, total_page = \
                super(PrimaryBiomarkersView, self).get_page_info(biomarker_class_list)

            biomarker_class_sublist = \
                super(PrimaryBiomarkersView, self).get_dmp_list_for_target_page(page, \
                    max_biomarker_num, biomarker_per_page, biomarker_class_list)

            probe_num = len(biomarker_class_list)
            gene_num = filter_biomarker_df["gene"].nunique()

            return render_template('base/primary_biomarkers.html', 
                biomarker_list=biomarker_class_sublist, 
                page=page, total_page=total_page, probe_num=probe_num,
                gene_num=gene_num, vis_data=str(vis_data))

class ValidationResultView(MainView):
    def get_df_on_conditions(self):
        input_csv = ""
        df = None
        cancer_type = request.cookies.get('cancerType')

        if cancer_type == "bladder":
            pass

        # elif cancer_type == "colorectal":
        #     df = validation_res_tables.colrectal_validation_result

        # elif cancer_type == "lung":
        #     df = validation_res_tables.lung_primary_biomarker_df

        # elif cancer_type == "liver":
        #     df = validation_res_tables.liver_primary_biomarker_df

        elif cancer_type == "pancreas":
            df = validation_res_tables.pancreas_validation_result

        else:
            df = validation_res_tables.colrectal_validation_result

        return df

    def get_data_from_csv(self):
        df = self.get_df_on_conditions()
        # filter_df = self.get_filter_dmp(df)
        biomarker_list = df.values
        biomarker_class_list = []
        
        for biomarker in biomarker_list:
            biomarker_class_list.append(ValidationRes(biomarker))

        # data for chromosome visualization

        return df, biomarker_class_list

    def post(self):
        df, biomarker_class_list = self.get_data_from_csv()
        page, max_biomarker_num, biomarker_per_page, total_page = \
            super(ValidationResultView, self).get_page_info(biomarker_class_list)

        biomarker_class_sublist = \
            super(ValidationResultView, self).get_dmp_list_for_target_page(page, \
                max_biomarker_num, biomarker_per_page, biomarker_class_list)

        probe_num = len(biomarker_class_list)
        gene_num = df["gene"].nunique()

        return render_template('base/validation_result.html', 
            biomarker_list=biomarker_class_sublist, 
            page=page, total_page=total_page, probe_num=probe_num,
            gene_num=gene_num)

blueprint.add_url_rule('/', view_func=MainView.as_view(MainView.__name__))
blueprint.add_url_rule('/plot', view_func=PlotView.as_view(PlotView.__name__))
blueprint.add_url_rule('/save', view_func=SaveDMPView.as_view(SaveDMPView.__name__))
blueprint.add_url_rule('/primaryBiomarker', view_func=PrimaryBiomarkersView.as_view(PrimaryBiomarkersView.__name__))
blueprint.add_url_rule('/validationResult', view_func=ValidationResultView.as_view(ValidationResultView.__name__))