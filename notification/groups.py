class GroupName:
	def __init__(self, model, id):
		self.model_name = model.__name__
		self.id = id
	
	def generate_group_name_for_all(self):
		return f"{self.model_name}_{self.id}_notify"

	def generate_group_name_for_master(self):
		return f"{self.model_name}_{self.id}_master_notify"

