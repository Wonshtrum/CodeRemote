from app import api
from typing import Optional


@api.get('/test/{test}')
def get_test(test: int, q: Optional[str] = None):
	return { 'test': test, 'q': q }
