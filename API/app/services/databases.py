from app.config import *


class DB:
	def __init__(self, url, port, user, pwd):
		raise NotImplementedError
	def insert(table, data):
		raise NotImplementedError
	def select(table, hash):
		raise NotImplementedError
	def delete(table, hash):
		raise NotImplementedError
	def watch(table):
		raise NotImplementedError

class MongoDB(DB):
	def __init__(self, url, port, user, pwd):
		import pymongo
		self.client = pymongo.MongoClient(url, port, username=user, password=pwd, authSource='admin')
		self.db = self.client[MONGO_DATABASE]
	def insert(self, table, data):
		collection = self.db[table]
		collection.insert(data)
	def watch(self, table):
		collection = self.db[table]
		with collection.watch([{'$match':{'operationType':'insert'}}]) as change_stream:
			for insert_change in change_stream:
				yield insert_change['fullDocument']

class RedisDB(DB):
	def __init__(self, url, port, user, pwd):
		import redis
		self.client = redis.Redis(host=url, port=port, password=pwd)
		self.pubsub = self.client.pubsub()
	def insert(self, table, data):
		self.client = redis.set(f'{table}.{data.hash}', data)
	def select(self, table, hash):
		return self.client.get(f'{table}.{hash}')
	def delete(self, table, hash):
		self.client.delete(f'{table}.{hash}')
	def watch(self, table):
		self.pubsub.subscribe(table)
		while True:
			yield self.pubsub.get_message()['data']


if DB_TYPE == 'Redis':
	db = RedisDB(DB_URL, DB_PORT, DB_USER, DB_PWD)
elif DB_TYPE == 'MongoDB':
	db = MongoDB(DB_URL, DB_PORT, DB_USER, DB_PWD)
else:
	raise ValueError(f'{DB_TYPE} is not a DB type supported.')