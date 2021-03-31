from databases import db
from nodes import distribute


for inserted_entry in db.watch('requests'):
	print(inserted_entry)
	distribute(inserted_entry)
