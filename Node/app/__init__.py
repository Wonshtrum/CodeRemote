from fastapi import FastAPI

print('app')
api = FastAPI()

import app.routes
