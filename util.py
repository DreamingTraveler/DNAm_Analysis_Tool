import config
import pandas as pd


class DMPTables():
	def __init__(self):
		self.colorectal_dmp_df = pd.read_csv(config.COLORECTAL_DMP_CSV)
		self.colorectal_asian_dmp_df = pd.read_csv(config.COLORECTAL_ASIAN_DMP_CSV)
		self.colorectal_white_dmp_df = pd.read_csv(config.COLORECTAL_WHITE_DMP_CSV)
		self.colorectal_black_dmp_df = pd.read_csv(config.COLORECTAL_BLACK_DMP_CSV)

		self.colorectal_early_stage_dmp_df = pd.read_csv(config.COLORECTAL_EARLY_STAGE_DMP_CSV)
		self.colorectal_late_stage_dmp_df = pd.read_csv(config.COLORECTAL_LATE_STAGE_DMP_CSV)

		# bladder
		self.bladder_dmp_df = pd.read_csv(config.BLADDER_DMP_CSV)
		self.bladder_asian_dmp_df = pd.read_csv(config.BLADDER_ASIAN_DMP_CSV)
		self.bladder_white_dmp_df = pd.read_csv(config.BLADDER_WHITE_DMP_CSV)
		self.bladder_black_dmp_df = pd.read_csv(config.BLADDER_BLACK_DMP_CSV)

		self.bladder_early_stage_dmp_df = pd.read_csv(config.BLADDER_EARLY_STAGE_DMP_CSV)
		self.bladder_late_stage_dmp_df = pd.read_csv(config.BLADDER_LATE_STAGE_DMP_CSV)

		# lung
		self.lung_dmp_df = pd.read_csv(config.LUNG_DMP_CSV)

		# liver
		self.liver_dmp_df = pd.read_csv(config.LIVER_DMP_CSV)

		# pancreas
		self.pancreas_dmp_df = pd.read_csv(config.PANCREAS_DMP_CSV)

		# prostate
		self.prostate_dmp_df = pd.read_csv(config.PROSTATE_DMP_CSV)

		# esophagus
		self.esophagus_dmp_df = pd.read_csv(config.ESOPHAGUS_DMP_CSV)

		# stomach
		self.stomach_dmp_df = pd.read_csv(config.STOMACH_DMP_CSV)

		# ovarian
		self.ovarian_dmp_df = pd.read_csv(config.OVARIAN_DMP_CSV)

		# breast
		self.breast_dmp_df = pd.read_csv(config.BREAST_DMP_CSV)

class BiomarkerTables():
	def __init__(self):
		self.colorectal_primary_biomarker_df = pd.read_csv(config.COLORECTAL_PRIMARY_BIOMARKER_CSV)
		self.colorectal_normal_beta_df = pd.read_csv(config.COLORECTAL_PRIMARY_BIOMARKER_NORMAL_BETA, index_col=0)
		self.colorectal_tumor_beta_df = pd.read_csv(config.COLORECTAL_PRIMARY_BIOMARKER_TUMOR_BETA, index_col=0)

		self.lung_primary_biomarker_df = pd.read_csv(config.LUNG_PRIMARY_BIOMARKER_CSV)
		self.lung_normal_beta_df = pd.read_csv(config.LUNG_PRIMARY_BIOMARKER_NORMAL_BETA, index_col=0)
		self.lung_tumor_beta_df = pd.read_csv(config.LUNG_PRIMARY_BIOMARKER_TUMOR_BETA, index_col=0)

		self.liver_primary_biomarker_df = pd.read_csv(config.LIVER_PRIMARY_BIOMARKER_CSV)
		self.liver_normal_beta_df = pd.read_csv(config.LIVER_PRIMARY_BIOMARKER_NORMAL_BETA, index_col=0)
		self.liver_tumor_beta_df = pd.read_csv(config.LIVER_PRIMARY_BIOMARKER_TUMOR_BETA, index_col=0)

		self.pancreas_primary_biomarker_df = pd.read_csv(config.PANCREAS_PRIMARY_BIOMARKER_CSV)
		self.pancreas_normal_beta_df = pd.read_csv(config.PANCREAS_PRIMARY_BIOMARKER_NORMAL_BETA, index_col=0)
		self.pancreas_tumor_beta_df = pd.read_csv(config.PANCREAS_PRIMARY_BIOMARKER_TUMOR_BETA, index_col=0)
		# self.colorectal_asian_dmp_df = pd.read_csv(config.COLORECTAL_ASIAN_DMP_CSV)
		# self.colorectal_white_dmp_df = pd.read_csv(config.COLORECTAL_WHITE_DMP_CSV)
		# self.colorectal_black_dmp_df = pd.read_csv(config.COLORECTAL_BLACK_DMP_CSV)

		# self.colorectal_early_stage_dmp_df = pd.read_csv(config.COLORECTAL_EARLY_STAGE_DMP_CSV)
		# self.colorectal_late_stage_dmp_df = pd.read_csv(config.COLORECTAL_LATE_STAGE_DMP_CSV)

		# bladder
		# self.bladder_dmp_df = pd.read_csv(config.BLADDER_DMP_CSV)
		# self.bladder_asian_dmp_df = pd.read_csv(config.BLADDER_ASIAN_DMP_CSV)
		# self.bladder_white_dmp_df = pd.read_csv(config.BLADDER_WHITE_DMP_CSV)
		# self.bladder_black_dmp_df = pd.read_csv(config.BLADDER_BLACK_DMP_CSV)

		# self.bladder_early_stage_dmp_df = pd.read_csv(config.BLADDER_EARLY_STAGE_DMP_CSV)
		# self.bladder_late_stage_dmp_df = pd.read_csv(config.BLADDER_LATE_STAGE_DMP_CSV)

class ValidationResultTables():
	def __init__(self):
		self.colrectal_validation_result = pd.read_csv(config.COLORECTAL_VALIDATION_RESULT)
		self.pancreas_validation_result = pd.read_csv(config.PANCREAS_VALIDATION_RESULT)