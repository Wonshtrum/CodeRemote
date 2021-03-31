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
		self.max_time = 20 #work.spec.time
		Thread.__init__(self)
		self.start()
		return True
	
	def __str__(self):
		if self.working:
			return bar((time()-self.start_time)/self.max_time)+' '+self.work.spec.hash
		else:
			return 'waiting...'


class Manager:
	def __init__(self, n):
		self.workers = [Worker(self) for _ in range(n)]
		self.status = {}
	
	def update(self, work, status, data=None):
		self.status[work.spec.hash] = (status, data)
	
	def submit(self, request):
		work = Work(request)
		for worker in self.workers:
			if not worker.working and worker.submit(work):
				return True
		return False
	
	def request(self, hash):
		result = self.status.get(hash)
		if result is not None and result[0] == Status.FINISHED:
			del self.status[hash]
		return result
	
	def get_load(self):
		workers = [str(worker) for worker in self.workers]
		return { 'workers': workers, 'work': self.status }
