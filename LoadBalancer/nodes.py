import requests as http
from multiprocessing import Queue
from threading import Thread
from time import sleep

Nodes = [
	'127.0.0.1'
]


TIMEOUT = 2
class Network:
	def __init__(self, nodes):
		# (free_containers, max_time_before_free_container)
		self.nodes = { node:None for node in nodes }
		self.requests = Queue()

	def distribute(self, request):
		self.requests.put(request)
	
	def pick_node(self):
		nodes = [ (node, state[0], state[1]) for node, state in self.nodes.items() if state is not None ]
		if not nodes:
			return None
		return max(nodes, key=lambda node: (node[1], -node[2]))[0]

	def send(self, request, node):
		result = http.put(node, data=request, timeout=TIMEOUT)
		print(result)
		if result.status_code != 202:
			self.requests.put(request)
	
	def process(self):
		while True:
			request = self.requests.get()
			while True:
				node = self.pick_node()
				if node is not None:
					break
				sleep(TIMEOUT)
			t = Thread(target=self.send, args=(request, node))
			t.start()
	
	def poll_node(self, node):
		result = http.get(node, timeout=TIMEOUT)
		print(result)
		if result.status_code == 200:
			status = result.json()
			self.nodes[node] = status.

	def poll(self):
		http.get()
