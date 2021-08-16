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
