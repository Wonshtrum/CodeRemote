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
			'limits.cpu': str(profile['cpu']),
			'limits.cpu.allowance': '50ms/100ms',
			'limits.memory': '100MB',
			'limits.memory.swap': 'false',
			'limits.processes': '10'
		}
	}
	container = client.containers.create(config, wait=True)
	container.start(wait=True)
	return container

def write_file(container, name, content):
	container.files.put(name, content)

def read_file(container, name):
	return container.files.get(name)

def execute(container, command, **kwargs):
	result = container.execute(command.split(), **kwargs)
	return result.exit_code, result.stdout, result.stderr

def destroy(container):
	container.stop(wait=True)
	container.delete()


contexts = {
	'python3': ContextPython,
	'c++': ContextCPP,
	'c': ContextC,
}


BASE_PATH = '/root/'
def run(request, timer):
	timer.start()
	state = "initializing"
	container = None
	try:
		context = contexts[request['lang']]
		print_err(context)
		context = context(request['files'])
		profile = request['profile']
		name = 'lxc'+request['hash'].replace('_','aa')
		container = create_container(name, context.image, profile)
		print_err("started")

		for file in request['files']:
			container.files.put(BASE_PATH+file['name'], file['content'])
		print_err("files written")
		exit_code, stdout, stderr = execute(container, f'ls -al {BASE_PATH}')
		print_err(exit_code)
		print_err(stdout)
		print_err(stderr)
		timer.end()

		state = "compilating"
		time_compile = 30
		for command in context.compile():
			print_err(command)
			exit_code, stdout, stderr = timeout(execute, time_compile)(container, command)
			print_err(exit_code)
			print_err(stdout)
			print_err(stderr)
			if exit_code != 0:
				raise ErrorWithStatus(Status.COMPILATION_FAILED, f"Compilation failed with code {exit_code}", stdout, stderr)
		timer.end()
		print_err("compiled")

		state = "executing"
		time_run = 30
		run_cmd = context.run()
		exit_code, stdout, stderr = timeout(execute, time_compile)(container, run_cmd)
		print_err(exit_code)
		print_err(stdout)
		print_err(stderr)
		if exit_code != 0:
			raise ErrorWithStatus(Status.CRASHED, f"Execution failed with code {exit_code}", stdout, stderr)
		timer.end()
		return ErrorWithStatus(Status.SUCCESS, stdout, stderr)

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
