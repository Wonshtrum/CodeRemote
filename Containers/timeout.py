import multiprocessing


SLACK = 1
def timeout(target, time):
	def wrapper(*args, **kwargs):
		queue = multiprocessing.Queue()
		def to_queue(*args, **kwargs):
			result = target(*args, **kwargs)
			queue.put(result)
		p = multiprocessing.Process(target=to_queue, args=args, kwargs=kwargs)
		p.start()
		p.join(time)
		if p.is_alive():
			p.terminate()
			p.join(SLACK)
			raise TimeoutError

		return queue.get(timeout=SLACK)
	return wrapper
