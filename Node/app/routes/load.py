from app import api, WorkManager


@api.get('/visual_load')
def get_visual_load():
	return WorkManager.get_visual_load()

@api.get('/load')
def get_load():
	return WorkManager.get_load()
