import pylxd
from time import sleep


client = pylxd.Client()


def list_all_containers():
	return client.containers.all()

def create_container(name, image, cpu):
	config = {'name': name, 'source': {'type': 'image', 'alias': image}, 'config': {'limits.cpu': str(cpu)}}
	return client.containers.create(config, wait=True)

def write_file(container, name, content):
	container.files.put(name, content)

def read_file(container, name):
	return container.files.get(name)

def execute(container, command):
	result = container.execute(command)
	return result.exit_code, result.stdout, result.stderr

def destroy(container):
	container.stop()
	container.delete()


images = {
	'python': 'pyAlpine',
	#'c++': 'cppAlpine',
	#'c': 'cAlpine',
}
BASE_PATH = '/root/'
def compile(request):
	image = images.get(request.lang)
	if image is None:
		return False
	container = create_container(request.hash, image, request.profile.cpu)

	for name, content in request.files:
		container.write_file(BASE_PATH+name, content)
	
	exit_code, stdout, stderr = execute(container, ['ls', '-al', BASE_PATH])
	sleep(10)
	destroy(container)

	return exit_code, stdout, stderr


if __name__ == '__main__'
	request = eval(input())
	compile(request)
