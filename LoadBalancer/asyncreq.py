import requests
from threading import Thread


class async_http:
	def __getattribute__(method):
		method = requests.__getattribute__(method)
		def async_request(*args, callback=None, **kwargs):
			if callback is not None:
				def _callback(response, *args, **kwargs):
					callback(response)
				kwargs['hooks'] = { 'response': _callback }
			t = Thread(target=method, args=args, kwargs=kwargs)
			t.start()
		return async_request
