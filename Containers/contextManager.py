class Context:
	image = None
	def __init__(self, progs):
		self.progs = [_['name'] for _ in progs]
		self.n = len(progs)
		self.init()
	def init(self):
		pass
	def compile(self):
		return []
	def run(self):
		raise NotImplementedError

class ContextPython(Context):
	image = "pyAlpine"
	def init(self):
		if self.n == 1:
			self.main = self.progs[0]
		elif "main.py" in self.progs:
			self.main = "main.py"
		else:
			raise Exception
	def run(self):
		return f"python3 {self.main}"

class ContextCPP(Context):
	image = "cppAlpine"
	def init(self):
		self.src = [prog for prog in self.progs if prog.endswith('.cpp')]
		self.compiled = "compiled"
	def compile(self):
		yield "g++ " + ' '.join(self.src) + f" -o {self.compiled}"
	def run(self):
		return f"./{self.compiled}"

def ContextC(Context):
	image = "cppAlpine"
	def init(self):
		self.src = [prog for prog in self.progs if prog.endswith('.c')]
		self.compiled = "compiled"
	def compile(self):
		yield "gcc " + ' '.join(self.src) + f" -o {self.compiled}"
	def run(self):
		return f"./{self.compiled}"
