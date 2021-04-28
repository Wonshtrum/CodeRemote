request = {
	'hash':'hash',
	'lang':'c++',
	'files': [
		{
			'name': 'main.cpp',
			'content': '#include <iostream>\nint main(){return 42;}'
		},
		{
			'name': 'module.py',
			'content': 'content2'
		}
	],
	'profile': {
		'cpu': 1,
		'ram': 200,
		'time': 30
	}
}

print(request)
