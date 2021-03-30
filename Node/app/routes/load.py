from app import api, WorkManager


@api.get('/load')
def get_ping():
	return WorkManager.get_load()
