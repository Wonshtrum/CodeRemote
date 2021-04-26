class Mock:
	def __init__(self, name='MOCK'):
		self._name = name
	def __getattribute__(self, name):
		if name == '_name':
			return object.__getattribute__(self, name)
		return Mock(self._name+'.'+name)
	def __call__(self, *args, **kwargs):
		print(self._name+'('+', '.join([str(arg) for arg in args]+[f'{name}={value}' for name, value in kwargs.items()])+')')
		return Mock(self._name+'()')
