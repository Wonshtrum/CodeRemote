import requests as http
from multiprocessing import Queue
from threading import Thread
from time import sleep
from asyncreq import async_http
from databases import db
from config import TIMEOUT


Nodes = [
	'127.0.0.1:8000'
]


class State:
	def __init__(self):
		self.capacity = 0
		self.time = 0
		self.missing_ping = 1
	def __str__(self):
		return f'({self.capacity}, {self.time}, {self.missing_ping})'
	def __repr__(self):
		return self.__str__()


class Network:
	def __init__(self, nodes):
		# (free_containers, max_time_before_free_container)
		self.nodes = { node:State() for node in nodes }
		self.requests = Queue()
		self.results = Queue()
	
	def start(self):
		self.process_thread = Thread(target=self.process, daemon=True)
		self.polling_thread = Thread(target=self.poll, daemon=True)
		self.process_thread.start()
		self.polling_thread.start()
		self.add_long_waiting_requests()
	
	def add_long_waiting_requests(self):
		for request in db.find_all('requests', state=0):
			print('Getting back:', request['hash'])
			self.requests.put(request)

	def distribute(self, request):
		del request['_id']
		self.requests.put(request)
	
	def pick_node(self):
		nodes = [ (node, state.capacity, state.time) for node, state in self.nodes.items() if state.missing_ping == 0 and state.capacity > 0 ]
		if not nodes:
			return None
		return max(nodes, key=lambda node: node[1])[0]

	def send(self, request, node):
		self.nodes[node].capacity -= 1
		try:
			result = http.put(f'http://{node}/work', json=request, timeout=TIMEOUT)
			if result.status_code == 202:
				db.update_one('requests', hash=request['hash'])(state=1)
			elif result.status_code == 422:
				print('DESTROYING', request['hash'])
				db.delete_all('requests', hash=request['hash'])
			else:
				result = None
		except Exception:
			result = None
		if result is None:
			sleep(TIMEOUT)
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
	
	def poll_node(self, node, verbose=False):
		while True:
			try:
				result = http.get(f'http://{node}/load', timeout=TIMEOUT)
			except Exception:
				result = None
			if verbose:
				print(f'waiting: {self.requests.qsize()}')
				print(self.nodes)
			state = self.nodes[node]
			if result is not None and result.status_code == 200:
				state.missing_ping = 0
				status = result.json()
				state.capacity = status['capacity']
				state.time = status['time']
				for hash, state in status['work'].items():
					if state == 1:
						self.results.put((node, hash))
			else:
				state.missing_ping += 1
			sleep(TIMEOUT)
	
	def publish(self, result):
		if result.status_code == 200:
			data = result.json()
			db.insert('results', data)
			#db.delete_all('requests', hash=data['hash'])
			db.update_one('requests', hash=data['hash'])(state=2)
		else:
			print('COULD NOT RETRIEVE A RESULT')

	def poll(self):
		self.thread_pool = [Thread(target=self.poll_node, args=(node, i==0)) for i, node in enumerate(self.nodes)]
		for t in self.thread_pool:
			t.start()

		while True:
			node, hash = self.results.get()
			data = { 'hash': hash }
			async_http.post(f'http://{node}/result', json=data, callback=self.publish)


network = Network(Nodes)
