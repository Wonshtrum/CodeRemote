from app import api, config
import uvicorn


if __name__ == '__main__':
	uvicorn.run(api, host=config.HOST, port=config.PORT)
