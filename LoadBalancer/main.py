from config import *
import pymongo


mongo = pymongo.MongoClient(MONGO_URL, MONGO_PORT, username=MONGO_USER, password=MONGO_PWD)
db = mongo[MONGO_DATABASE]
requests = db['requests']

print('start')
with requests.watch([{'$match':{'operationType':'insert'}}]) as change_stream:
	for insert_change in change_stream:
		print(insert_change)
		inserted_entry = insert_change['fullDocument']
		print(inserted_entry)
print('end')
