import pylxd
from mock import Mock


try:
	client = pylxd.Client()
except Exception:
	client = Mock()


def execute(
		self,
		commands,
		environment=None,
		encoding=None,
		decode=True,
		stdin_payload=None,
		stdin_encoding="utf-8",
		stdout_handler=None,
		stderr_handler=None,
		user=None,
		group=None,
		cwd=None,
	):
		"""Execute a command on the instance. stdout and stderr are buffered if
		no handler is given.
		:param commands: The command and arguments as a list of strings
		:type commands: [str]
		:param environment: The environment variables to pass with the command
		:type environment: {str: str}
		:param encoding: The encoding to use for stdout/stderr if the param
			decode is True.  If encoding is None, then no override is
			performed and whatever the existing encoding from LXD is used.
		:type encoding: str
		:param decode: Whether to decode the stdout/stderr or just return the
			raw buffers.
		:type decode: bool
		:param stdin_payload: Payload to pass via stdin
		:type stdin_payload: Can be a file, string, bytearray, generator or
			ws4py Message object
		:param stdin_encoding: Encoding to pass text to stdin (default utf-8)
		:param stdout_handler: Callable than receive as first parameter each
			message received via stdout
		:type stdout_handler: Callable[[str], None]
		:param stderr_handler: Callable than receive as first parameter each
			message received via stderr
		:type stderr_handler: Callable[[str], None]
		:param user: User to run the command as
		:type user: int
		:param group: Group to run the command as
		:type group: int
		:param cwd: Current working directory
		:type cwd: str
		:returns: A tuple of `(exit_code, stdout, stderr)`
		:rtype: _InstanceExecuteResult() namedtuple
		"""
		if isinstance(commands, str):
			raise TypeError("First argument must be a list.")
		if environment is None:
			environment = {}

		response = self.api["exec"].post(
			json={
				"command": commands,
				"environment": environment,
				"wait-for-websocket": True,
				"interactive": False,
				"user": user,
				"group": group,
				"cwd": cwd,
			}
		)

		fds = response.json()["metadata"]["metadata"]["fds"]
		operation_id = Operation.extract_operation_id(response.json()["operation"])
		parsed = parse.urlparse(
			self.client.api.operations[operation_id].websocket._api_endpoint
		)

		with managers.web_socket_manager(WebSocketManager()) as manager:
			stdin = _StdinWebsocket(
				self.client.websocket_url,
				payload=stdin_payload,
				encoding=stdin_encoding,
			)
			stdin.resource = "{}?secret={}".format(parsed.path, fds["0"])
			stdin.connect()
			stdout = _CommandWebsocketClient(
				manager,
				self.client.websocket_url,
				encoding=encoding,
				decode=decode,
				handler=stdout_handler,
			)
			stdout.resource = "{}?secret={}".format(parsed.path, fds["1"])
			stdout.connect()
			stderr = _CommandWebsocketClient(
				manager,
				self.client.websocket_url,
				encoding=encoding,
				decode=decode,
				handler=stderr_handler,
			)
			stderr.resource = "{}?secret={}".format(parsed.path, fds["2"])
			stderr.connect()

			manager.start()

			# watch for the end of the command:
			while True:
				operation = self.client.operations.get(operation_id)
				if "return" in operation.metadata:
					break
				time.sleep(0.5)  # pragma: no cover

			try:
				stdin.close()
			except BrokenPipeError:
				pass

			stdout.finish_soon()
			stderr.finish_soon()
			try:
				manager.close_all()
			except BrokenPipeError:
				pass

			while not stdout.finished or not stderr.finished:
				time.sleep(0.1)  # progma: no cover

			manager.stop()
			manager.join()

			return _InstanceExecuteResult(
				operation.metadata["return"], stdout.data, stderr.data
			)

