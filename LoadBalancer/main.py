from DB import db


print('start')

for inserted_entry in db.watch('requests'):
	print(inserted_entry)

print('end')
