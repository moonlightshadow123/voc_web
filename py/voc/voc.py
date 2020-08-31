from mwapi import MWapi
from sc import SC
from utils import getFilePath
getFilePath(__file__)

class VOC:
	def __init__(self, temp_dir, temp_url):
		self.sc = SC()
		self.mwapi = MWapi(temp_dir, temp_url)

	def lookup(self, word):
		res = {"sc":None, "api":None}
		iscorrect, res_sc = self.sc.check(word)
		if not iscorrect:
			# res["candi"] = res_sc
			res = {"sc":res_sc}
			return res
		res_api = self.mwapi.lookup(word, mode="json")
		res["voc"] = res_api
		return res

