import config
import pandas as pd


class DMPTables():
	def __init__(self):
		self.colorectal_dmp_df = pd.read_csv(config.COLORECTAL_DMP_CSV)
		self.bladder_dmp_df = pd.read_csv(config.BLADDER_DMP_CSV)
