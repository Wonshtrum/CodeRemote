from patch_lxd import pylxd, client
from time import time
from contextManager import *
from timeout import timeout
import sys


print_err = lambda *args, **kwargs: print(*args, **kwargs, file=sys.stderr)


class Status:
	SUCCESS = 0
	COMPILATION_FAILED = 1
	CRASHED = 2
	LIMIT_REACHED = 3
	GENERIC_ERROR = 4

class ErrorWithStatus(Exception):
	def __init__(self, status, msg=None, out=None, err=None):
		super().__init__()
		self.status = status
		self.msg = msg
		self.out = out
		self.err = err

class Timer:
	def __init__(self):
		self.time = None
		self.steps = []
	def start(self):
		self.time = time()
	def end(self):
		tmp = time()
		self.steps.append(tmp-self.time)
		self.time = tmp

class TimeKeeper:
	def __init__(self, max_time):
		self.time = max_time
		self.start = time()
	def advance(self):
		self.start = time()
		return max(0, self.time)
	def suspend(self):
		self.time -= time()-self.start

def list_all_containers():
	return client.containers.all()

def create_container(name, image, profile):
	#https://lxd.readthedocs.io/en/stable-3.0/containers/
	config = {
		'name': name,
		'source': {
			'type': 'image',
			'alias': image
		},
		'config': {
			'limits.cpu': '1',
			'limits.cpu.allowance': f'{int(profile["cpu"]*100)}ms/100ms',
			'limits.memory': f'{profile["ram"]}MB',
			'limits.memory.swap': 'false',
			'limits.processes': '100'
		}
	}
	print_err(config)
	container = client.containers.create(config, wait=True)
	container.start(wait=True)
	return container

def write_file(container, name, content):
	container.files.put(name, content)

def read_file(container, name):
	return container.files.get(name)

def execute(container, command, **kwargs):
	result = container.execute(["su", "-", "nobody", "-c", command], **kwargs)
	return result.exit_code, result.stdout, result.stderr

def destroy(container):
	container.stop(wait=True)
	container.delete()

def debug_ls(container, path):
	exit_code, stdout, stderr = execute(container, f'ls -al {path}')
	print_err(exit_code)
	print_err(stdout)
	print_err(stderr)


contexts = {
	'python3': ContextPython,
	'c++': ContextCPP,
	'c': ContextC,
}


BASE_PATH = '/home/nobody'
def run(request, timer):
	timer.start()
	state = "initializing"
	container = None
	profile = request['profile']
	max_time = profile['time']
	try:
		context = contexts[request['lang']]
		print_err(context)
		context = context(request['files'])
		name = 'lxc'+request['hash'].replace('_','aa')
		container = create_container(name, context.image, profile)
		print_err("started")

		for file in request['files']:
			container.files.put(BASE_PATH+file['name'], file['content'], uid=65534)
		timer.end()
		print_err("files written")
		debug_ls(container, BASE_PATH)

		state = "compilating"
		time_compile = TimeKeeper(max_time)
		for command in context.compile():
			print_err(command)
			exit_code, stdout, stderr = timeout(execute, time_compile.advance())(container, command)
			time_compile.suspend()
			print_err(exit_code)
			print_err(stdout)
			print_err(stderr)
			if exit_code != 0:
				raise ErrorWithStatus(Status.COMPILATION_FAILED, f"Compilation failed with code {exit_code}", stdout, stderr)
		timer.end()
		print_err("compiled")
		debug_ls(container, BASE_PATH)

		state = "executing"
		time_run = TimeKeeper(max_time)
		run_cmd = context.run()
		exit_code, stdout, stderr = timeout(execute, time_run.advance())(container, run_cmd)
		time_run.suspend()
		timer.end()
		print_err(exit_code)
		print_err(stdout)
		print_err(stderr)
		if exit_code != 0:
			raise ErrorWithStatus(Status.CRASHED, f"Execution failed with code {exit_code}", stdout, stderr)
		return ErrorWithStatus(Status.SUCCESS, None, stdout, stderr)

	except ErrorWithStatus as error:
		return error
	except TimeoutError as error:
		return ErrorWithStatus(Status.LIMIT_REACHED, f"Timeout reached while {state}")
	except Exception as error:
		print_err("Error:", type(error), error)
		return ErrorWithStatus(Status.GENERIC_ERROR, "The system couldn't initialize an execution environment for your request. If you think the error is not in your code, please retry submitting it.")
	finally:
		timer.end()
		print_err("finished")
		if container is not None:
			destroy(container)
			print_err("destroyed")


if __name__ == '__main__':
	request = input()
	print_err(request)
	request = eval(request)
	timer = Timer()
	result = run(request, timer)
	timer.steps.extend([0,0,0])
	init_time, compilation_time, execution_time, *_ = timer.steps
	logs = {
		'status':result.status,
		'message':result.msg,
		'init_time':init_time,
		'compilation_time':compilation_time,
		'execution_time':execution_time
	}
	final = {
		'stdout':result.out,
		'stderr':result.err,
		'logs':logs
	}
	print(repr(final))
