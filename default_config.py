DEBUG = True
SECRET_KEY = 'c882369d7b66e8697426c3e8fb2675c0'

UPLOAD_FOLDER = './static/upload/dmp_tables_operation'
ALLOWED_EXTENSIONS = {'xlsx', 'csv'}

SUB_DF_COLUMNS = ["Probe_ID", "logFC", "t", "adj.P.Val", "CHR", \
"MAPINFO", "gene", "feat.cgi", "feature", "cgi"]
PRIMARY_BIOMARKERS_COLUMNS = ["Probe_ID", "beta_diff", "t", "adj.P.Val", \
"gene", "feat.cgi", "chr", "coord", "is_candidate"]

DATA_PATH = "static/data/"

# colorectal cancer DNAm analysis result files
COLORECTAL_DMP_CSV = DATA_PATH + "colorectal/colorectal_DMP_analysis_result_TN.csv"

# primary biomarker info
COLORECTAL_PRIMARY_BIOMARKER_CSV = DATA_PATH + "colorectal/colorectal_primary_biomarkers.csv"
COLORECTAL_PRIMARY_BIOMARKER_NORMAL_BETA = \
	DATA_PATH + "colorectal/colorectal_primary_biomarkers_normal_beta.csv"

COLORECTAL_PRIMARY_BIOMARKER_TUMOR_BETA = \
	DATA_PATH + "colorectal/colorectal_primary_biomarkers_tumor_beta.csv"

# validation result
COLORECTAL_VALIDATION_RESULT = DATA_PATH + "colorectal/colorectal_validation_result.csv"

# racial data
COLORECTAL_ASIAN_DMP_CSV = DATA_PATH + "colorectal/colorectal_asian_DMP_analysis_result_TN.csv"
COLORECTAL_WHITE_DMP_CSV = DATA_PATH + "colorectal/colorectal_white_DMP_analysis_result_TN.csv"
COLORECTAL_BLACK_DMP_CSV = DATA_PATH + "colorectal/colorectal_black_DMP_analysis_result_TN.csv"

# stage data
COLORECTAL_EARLY_STAGE_DMP_CSV = \
DATA_PATH + "colorectal/colorectal_stage_I&II_DMP_analysis_result_TN.csv"
COLORECTAL_LATE_STAGE_DMP_CSV = \
DATA_PATH + "colorectal/colorectal_stage_III&IV_DMP_analysis_result_TN.csv"

# bladder
BLADDER_DMP_CSV = DATA_PATH + "bladder/bladder_DMP_analysis_result_TN.csv"

# racial data
BLADDER_ASIAN_DMP_CSV = DATA_PATH + "bladder/bladder_asian_DMP_analysis_result_TN.csv"
BLADDER_WHITE_DMP_CSV = DATA_PATH + "bladder/bladder_white_DMP_analysis_result_TN.csv"
BLADDER_BLACK_DMP_CSV = DATA_PATH + "bladder/bladder_black_DMP_analysis_result_TN.csv"

# stage data
BLADDER_EARLY_STAGE_DMP_CSV = \
DATA_PATH + "bladder/bladder_stage_I&II_DMP_analysis_result_TN.csv"
BLADDER_LATE_STAGE_DMP_CSV = \
DATA_PATH + "bladder/bladder_stage_III&IV_DMP_analysis_result_TN.csv"

# lung
LUNG_DMP_CSV = DATA_PATH + "lung/lung_DMP_analysis_result_TN.csv"
# primary biomarker info
LUNG_PRIMARY_BIOMARKER_CSV = DATA_PATH + "lung/lung_primary_biomarkers.csv"
LUNG_PRIMARY_BIOMARKER_NORMAL_BETA = \
	DATA_PATH + "lung/lung_primary_biomarkers_normal_beta.csv"

LUNG_PRIMARY_BIOMARKER_TUMOR_BETA = \
	DATA_PATH + "lung/lung_primary_biomarkers_tumor_beta.csv"

# liver
LIVER_DMP_CSV = DATA_PATH + "liver/liver_DMP_analysis_result_TN.csv"
LIVER_PRIMARY_BIOMARKER_CSV = DATA_PATH + "liver/liver_primary_biomarkers.csv"
LIVER_PRIMARY_BIOMARKER_NORMAL_BETA = \
	DATA_PATH + "liver/liver_primary_biomarkers_normal_beta.csv"

LIVER_PRIMARY_BIOMARKER_TUMOR_BETA = \
	DATA_PATH + "liver/liver_primary_biomarkers_tumor_beta.csv"


# pancreas
PANCREAS_DMP_CSV = DATA_PATH + "pancreas/pancreas_DMP_analysis_result_TN.csv"
PANCREAS_PRIMARY_BIOMARKER_CSV = DATA_PATH + "pancreas/pancreas_primary_biomarkers.csv"
PANCREAS_PRIMARY_BIOMARKER_NORMAL_BETA = \
	DATA_PATH + "pancreas/pancreas_primary_biomarkers_normal_beta.csv"

PANCREAS_PRIMARY_BIOMARKER_TUMOR_BETA = \
	DATA_PATH + "pancreas/pancreas_primary_biomarkers_tumor_beta.csv"
	
PANCREAS_VALIDATION_RESULT = DATA_PATH + "pancreas/pancreas_validation_result.csv"
# prostate
PROSTATE_DMP_CSV = DATA_PATH + "prostate/prostate_DMP_analysis_result_TN.csv"
# PROSTATE_PRIMARY_BIOMARKER_CSV = DATA_PATH + "prostate/prostate_primary_biomarkers.csv"
# PROSTATE_PRIMARY_BIOMARKER_NORMAL_BETA = \
# 	DATA_PATH + "prostate/prostate_primary_biomarkers_normal_beta.csv"

# PROSTATE_PRIMARY_BIOMARKER_TUMOR_BETA = \
# 	DATA_PATH + "prostate/prostate_primary_biomarkers_tumor_beta.csv"

# esophagus
ESOPHAGUS_DMP_CSV = DATA_PATH + "esophagus/esophagus_DMP_analysis_result_TN.csv"
# esophagus_PRIMARY_BIOMARKER_CSV = DATA_PATH + "esophagus/esophagus_primary_biomarkers.csv"
# esophagus_PRIMARY_BIOMARKER_NORMAL_BETA = \
# 	DATA_PATH + "esophagus/esophagus_primary_biomarkers_normal_beta.csv"

# esophagus_PRIMARY_BIOMARKER_TUMOR_BETA = \
# 	DATA_PATH + "esophagus/esophagus_primary_biomarkers_tumor_beta.csv"

# stomach
STOMACH_DMP_CSV = DATA_PATH + "stomach/stomach_DMP_analysis_result_TN.csv"

# ovarian
OVARIAN_DMP_CSV = DATA_PATH + "ovarian/ovarian_DMP_analysis_result_TN.csv"

# breast
BREAST_DMP_CSV = DATA_PATH + "breast/breast_DMP_analysis_result_TN.csv"

OST_DMP_CSV = DATA_PATH + "osteoporosis/osteoporosis_DMP_analysis_result.csv"

BRAIN_DMP_CSV = DATA_PATH + "brain/brain_DMP_analysis_result.csv"

KIDNEY_DMP_CSV = DATA_PATH + "kidney/kidney_DMP_analysis_result.csv"