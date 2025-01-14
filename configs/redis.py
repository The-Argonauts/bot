import redis

class RedisClient:
    def __init__(self, host="localhost", port=6379, db=0):
        self._host = host
        self._port = port
        self._db = db
        self._connection = None

    def connect(self):
        if not self._connection:
            self._connection = redis.StrictRedis(host=self._host, port=self._port, db=self._db, decode_responses=True)
        return self._connection

    def get_connection(self):
        if not self._connection:
            self.connect()
        return self._connection
