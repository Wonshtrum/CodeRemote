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
		try:
			if exit == 0:
				return eval(stdout)
			raise Exception
		except Exception:
			logs = {
				'status':4,
				'message':'The manager resjected your request for an unknown reason.'
				'init_time':0,
				'compilation_time':0,
				'execution_time':0
			}
			result = {
				'stdout':None,
				'stderr':None,
				'logs':logs
			}
			return result
	
	def __hash__(self):
		return hash(self.spec.hash)
