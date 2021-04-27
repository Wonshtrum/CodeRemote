import pylxd
from time import sleep
from mock import Mock
from contextManager import *
from timeout import timeout


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
SLACK = 2
def run(request):
	context = contexts.get(request['lang'])
	print(context)
	context = context(request['files'])
	if context is None:
		return False
	profile = request['profile']
	container = create_container(request['hash'], context.image, profile)
	print("started")

	try:
		for file in request['files']:
			container.files.put(BASE_PATH+file['name'], file['content'])
		print("files written")
		exit_code, stdout, stderr = execute(container, f'ls -al {BASE_PATH}')
		print(exit_code)
		print(stdout)
		print(stderr)

		time_compile = 5
		for command in context.compile():
			res = timeout(execute, time_compile)(container, command)
			print('compilation:', res)
		print("compiled")
		time_run = 5
		run_cmd = context.run()
		exit_code, stdout, stderr = timeout(execute, time_compile+SLACK)(container, f'timeout -s SIGKILL {time_run} {run_cmd}')
		print(exit_code)
		print(stdout)
		print(stderr)
	except Exception as error:
		print('Error:', error)


	print("finished")
	destroy(container)
	print("destroyed")

	return None


if __name__ == '__main__':
	request = eval(input())
	run(request)
