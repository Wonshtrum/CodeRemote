from app import config
from time import sleep
import subprocess as sp


class Work:
	def __init__(self, spec):
		self.spec = spec

	def process(self, update):
		proc = sp.Popen([config.EXEC_BIN, config.EXEC_FILE], stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, encoding = 'utf8')
		stdout, stderr = proc.communicate(repr(self.spec.dict()))
		with open('log', 'w') as f:
			f.write(stdout)
			f.write('\n///////////////////////////////////////////\n')
			f.write(stderr)
		exit = proc.poll()
		result = None
		if exit is None:
			proc.kill()
		try:
			if exit == 0:
				result = eval(stdout)
			else:
				raise Exception
		except Exception as error:
			print(exit, error)
			logs = {
				'status':4,
				'message':'The manager rejected your request for an unknown reason.',
				'init_time':0,
				'compilation_time':0,
				'execution_time':0
			}
			result = {
				'stdout':None,
				'stderr':None,
				'logs':logs
			}
		finally:
			result['logs'].update(self.spec.dict())
			return result
	
	def __hash__(self):
		return hash(self.spec.hash)
