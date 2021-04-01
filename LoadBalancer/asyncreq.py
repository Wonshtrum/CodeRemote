import requests
from threading import Thread


class _async_http(type):
	def __getattribute__(cls, method):
		method = requests.__getattribute__(method)
		def async_request(*args, callback=None, **kwargs):
			if callback is not None:
				def _callback(response, *args, **kwargs):
					callback(response)
				kwargs['hooks'] = { 'response': _callback }
			t = Thread(target=method, args=args, kwargs=kwargs)
			t.start()
		return async_request

class async_http(metaclass=_async_http):
	pass
