from threading import Thread
from app.services.work import Work
from time import time


def bar(progress, n = 10):
	return '['+'='*int(progress*n)+'>'+'.'*int(n-progress*n)+']'

class Status:
	SUBMITTED = 0
	FINISHED = 1


class Worker(Thread):
	def __init__(self, manager):
		self.manager = manager
		self.work = None
		self.start_time = None
		self.max_time = None
		self.working = False

	def run(self):
		self.start_time = time()
		self.manager.update(self.work, Status.SUBMITTED)
		data = self.work.process(self.manager.update)
		self.manager.update(self.work, Status.FINISHED, data)
		self.working = False

	def submit(self, work):
		if self.working:
			return False
		self.working = True
		self.work = work
		self.max_time = work.spec.profile.time
		Thread.__init__(self)
		self.start()
		return True
	
	def max_time_left(self):
		if self.working:
			return self.start_time+self.max_time-time()
		return 0
	
	def __str__(self):
		if self.working:
			return bar((time()-self.start_time)/self.max_time)+' '+self.work.spec.hash
		else:
			return 'waiting...'


class Manager:
	def __init__(self, n):
		self.workers = [Worker(self) for _ in range(n)]
		self.status = {}
		self.data = {}
	
	def update(self, work, status, data=None):
		self.status[work.spec.hash] = status
		self.data[work.spec.hash] = data
	
	def submit(self, request):
		work = Work(request)
		for worker in self.workers:
			if not worker.working and worker.submit(work):
				return True
		return False
	
	def request(self, hash):
		result = self.status.get(hash), self.data.get(hash)
		if result[0] == Status.FINISHED:
			del self.status[hash]
			del self.data[hash]
		return result
	
	def get_visual_load(self):
		workers = [str(worker) for worker in self.workers]
		return { 'workers': workers, 'work': self.status }
	
	def get_load(self):
		capacity = sum(1 for worker in self.workers if not worker.working)
		time = 0
		if capacity == 0:
			time = min(worker.max_time_left() for worker in self.workers)
		return { 'capacity': capacity, 'time': time, 'work': self.status }
