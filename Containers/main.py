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
	return client.containers.create(config, wait=True)

def write_file(container, name, content):
	container.files.put(name, content)

def read_file(container, name):
	return container.files.get(name)

def execute(container, command):
	result = container.execute(command.split())
	return result.exit_code, result.stdout, result.stderr

def destroy(container):
	container.stop()
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

	try:
		for file in request['files']:
			container.write_file(BASE_PATH+file['name'], file['content'])
	
		exit_code, stdout, stderr = execute(container, f'ls -al {BASE_PATH}')

		time_compile = 5
		for command in context.compile():
			res = timeout(execute, time_compile)(container, command)
			print('compilation:', res)
		time_run = 5
		run_cmd = context.run()
		res = timeout(execute, time_compile+SLACK)(container, f'timeout {time_run} {run_cmd}')
		print('execution:', res)
	except Exception as error:
		print('Error:', error)


	destroy(container)

	return exit_code, stdout, stderr


if __name__ == '__main__':
	request = eval(input())
	run(request)
