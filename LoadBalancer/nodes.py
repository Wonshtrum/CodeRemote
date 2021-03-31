import requests as http
from multiprocessing import Queue
from threading import Thread


Nodes = [
	'127.0.0.1'
]


class Network:
	def __init__(self, nodes):
		self.nodes = nodes
		self.requests = Queue()

	def distribute(self, request):
		self.requests.put(request)
	
	def pick_node(self):
		return self.nodes[0]

	def send(self, request, node):
		result = http.put(node, data=request, timeout=2)
		print(result)
		if result.status_code != 202:
			self.requests.put(request)
	
	def process(self):
		while True:
			request = self.requests.get()
			t = Thread(target=self.send, args=(request, self.pick_node()))
			t.start()
	
	def poll(self):
		pass
