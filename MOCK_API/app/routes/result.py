from app import api
from pydantic import BaseModel
from random import choice

class Demande(BaseModel):
	hash: str


SUCCESS = {
	'stdout': 'Hello world!\n'*20,
	'stderr': 'aucune erreur!',
	'logs': {
		'status': 0,
		'message': 'Code successfully ran!',
		'compilation_time': 3.64,
		'execution_time': 14.12,
	}
}

COMPILATION_FAILED = {
	'stdout': '',
	'stderr': """
	""",
	'logs': {
		'status': 1,
		'message': 'Code didn\'t compiled...',
		'compilation_time': 3.64,
		'execution_time': 0,
	}
}

CRASHED = {
	'stdout': 'Hello world!\n'*20,
	'stderr': """Traceback (most recent call last):                                                                                                   
File "main.py", line 12, in <module>                                                                                                 
  for insert_change in change_stream:                                                                                                
File "/home/pfe/LB/LoadBalancer/venv/lib/python3.6/site-packages/pymongo/change_stream.py", line 249, in next                        
  doc = self.try_next()                                                                                                              
File "/home/pfe/LB/LoadBalancer/venv/lib/python3.6/site-packages/pymongo/change_stream.py", line 303, in try_next                    
  change = self._cursor._try_next(True)                                                                                              
File "/home/pfe/LB/LoadBalancer/venv/lib/python3.6/site-packages/pymongo/command_cursor.py", line 270, in _try_next                  
  self._refresh()                                                                                                                    
File "/home/pfe/LB/LoadBalancer/venv/lib/python3.6/site-packages/pymongo/command_cursor.py", line 206, in _refresh                   
  False))                                                                                                                            
File "/home/pfe/LB/LoadBalancer/venv/lib/python3.6/site-packages/pymongo/command_cursor.py", line 140, in __send_message             
  operation, self._unpack_response, address=self.__address)                                                                          
File "/home/pfe/LB/LoadBalancer/venv/lib/python3.6/site-packages/pymongo/mongo_client.py", line 1372, in _run_operation_with_response
  exhaust=exhaust)                                                                                                                   
File "/home/pfe/LB/LoadBalancer/venv/lib/python3.6/site-packages/pymongo/mongo_client.py", line 1471, in _retryable_read             
  return func(session, server, sock_info, slave_ok)                                                                                  
File "/home/pfe/LB/LoadBalancer/venv/lib/python3.6/site-packages/pymongo/mongo_client.py", line 1366, in _cmd                        
  unpack_res)                                                                                                                        
File "/home/pfe/LB/LoadBalancer/venv/lib/python3.6/site-packages/pymongo/server.py", line 117, in run_operation_with_response        
  reply = sock_info.receive_message(request_id)                                                                                      
File "/home/pfe/LB/LoadBalancer/venv/lib/python3.6/site-packages/pymongo/pool.py", line 726, in receive_message                      
  self._raise_connection_failure(error)                                                                                              
File "/home/pfe/LB/LoadBalancer/venv/lib/python3.6/site-packages/pymongo/pool.py", line 724, in receive_message                      
  return receive_message(self, request_id, self.max_message_size)                                                                    
File "/home/pfe/LB/LoadBalancer/venv/lib/python3.6/site-packages/pymongo/network.py", line 195, in receive_message                   
  _receive_data_on_socket(sock_info, 16, deadline))                                                                                  
File "/home/pfe/LB/LoadBalancer/venv/lib/python3.6/site-packages/pymongo/network.py", line 286, in _receive_data_on_socket           
  chunk_length = sock_info.sock.recv_into(mv[bytes_read:])                                                                           
	""",
	'logs': {
		'status': 2,
		'message': 'Code crashed while running...',
		'compilation_time': 0,
		'execution_time': 0.68,
	}
}

LIMIT_REACHED = {
	'stdout': 'Hello world!\n'*20,
	'stderr': 'en cours d\'execution...\n'*50,
	'logs': {
		'status': 3,
		'message': 'Code excedeed time constraint!',
		'compilation_time': 4.46,
		'execution_time': 30.02,
	}
}

@api.post('/result')
async def put_request(dem: Demande):
	return {"status": "Successfully got the logs", "data":choice([SUCCESS, COMPILATION_FAILED, CRASHED, LIMIT_REACHED])}
