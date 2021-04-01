from databases import db
from nodes import network


network.start()
for inserted_entry in db.watch('requests'):
	print(inserted_entry)
	network.distribute(inserted_entry)
