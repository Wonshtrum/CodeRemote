from app import api, config
import uvicorn


if __name__ == '__main__':
	uvicorn.run("main:api", host=config.HOST, port=config.PORT, reload=True)
