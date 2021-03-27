from app import api


pings = 0
@api.get('/ping')
def get_ping():
	global pings
	pings += 1
	return { 'pong': pings }
