from app import api, config
import uvicorn
from sys import argv


if __name__ == '__main__':
	port = config.PORT
	if len(argv) > 1:
		port = int(argv[1])
	uvicorn.run(api, host=config.HOST, port=port)
