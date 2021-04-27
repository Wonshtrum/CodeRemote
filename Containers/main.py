import pylxd
from time import time
from mock import Mock
from contextManager import *
from timeout import timeout


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


try:
	client = pylxd.Client()
except Exception:
	client = Mock()

def list_all_containers():
	return client.containers.all()

def create_container(name, image, profile):
	#https://lxd.readthedocs.io/en/stable-3.0/containers/
	#limits.cpu.allowance 10ms/100ms
	#limits.memory 100MB
	#limits.processes
	config = {'name': name, 'source': {'type': 'image', 'alias': image}, 'config': {'limits.cpu': str(profile['cpu'])}}
	container = client.containers.create(config, wait=True)
	container.start(wait=True)
	return container

def write_file(container, name, content):
	container.files.put(name, content)

def read_file(container, name):
	return container.files.get(name)

def execute(container, command):
	result = container.execute(command.split())
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
		print(context)
		context = context(request['files'])
		profile = request['profile']
		container = create_container(request['hash'], context.image, profile)
		print("started")

		for file in request['files']:
			container.files.put(BASE_PATH+file['name'], file['content'])
		print("files written")
		exit_code, stdout, stderr = execute(container, f'ls -al {BASE_PATH}')
		print(exit_code)
		print(stdout)
		print(stderr)
		timer.end()

		state = "compilating"
		time_compile = 5
		for command in context.compile():
			exit_code, stdout, stderr = timeout(execute, time_compile)(container, command)
			print(exit_code)
			print(stdout)
			print(stderr)
			if exit_code != 0:
				raise ErrorWithStatus(Status.COMPILATION_FAILED, f"Compilation failed with code {exit_code}", stdout, stderr)
		timer.end()
		print("compiled")

		state = "executing"
		time_run = 5
		run_cmd = context.run()
		exit_code, stdout, stderr = timeout(execute, time_compile)(container, run_cmd)
		print(exit_code)
		print(stdout)
		print(stderr)
		if exit_code != 0:
			raise ErrorWithStatus(Status.CRASHED, f"Execution failed with code {exit_code}", stdout, stderr)
		timer.end()
		return ErrorWithStatus(Status.SUCCESS)

	except ErrorWithStatus as error:
		return error
	except TimeoutError as error:
		return ErrorWithStatus(Status.LIMIT_REACHED, f"Timeout reached while {state}")
	except Exception as error:
		print("Error:", type(error), error)
		return ErrorWithStatus(Status.GENERIC_ERROR, "The system couldn't initialize an execution environment for your request. If you think the error is not in your code, please retry submitting it.")
	finally:
		timer.end()
		print("finished")
		if container is not None:
			destroy(container)
			print("destroyed")


if __name__ == '__main__':
	request = eval(input())
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
