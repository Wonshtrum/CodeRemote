from time import sleep


MAX_TIME = 20
class Work:
	def __init__(self, spec):
		self.spec = spec

	def process(self, update):
		sleep(30)
		for file in self.spec.files:
			print(file.name, file.content)
		return ('this is a random stdout', 'this is a random stderr')
	
	def __hash__(self):
		return hash(self.spec.hash)
