from app import config
from time import sleep
import subprocess as sp


MAX_TIME = 20
class Work:
	def __init__(self, spec):
		self.spec = spec

	def process(self, update):
		proc = sp.Popen(f"exec python3 {config.EXEC_PATH}", stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, encoding = 'utf8')
		stdout, stderr = proc.communicate(repr(self.spec))
		exit = proc.poll()
		if exit is None:
			proc.kill()
		return (stdout, stderr)
	
	def __hash__(self):
		return hash(self.spec.hash)
