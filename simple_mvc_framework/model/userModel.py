from init import *

conf = I('conf')

class userModel(conf):
	def __init__(self):
		super().__init__('userList.conf')
		self.getName = super().__getitem__
		self.add = super().__setitem__
		self.remove = super().__delitem__