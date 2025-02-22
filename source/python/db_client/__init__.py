# Import 3rd-party libraries
import psycopg

class DBClient:
    hostname: str
    port: int
    dbname: str
    user: str
    password: str

    def __init__(
            self,
            password: str,
            dbname: str,
            hostname: str = ...,
            port: int = ...,
            user: str = ...
    ):
        self.hostname = hostname if hostname is not ... else "localhost"
        self.port = port if port is not ... else 5432
        self.user = user if user is not ... else "postgres"
        self.password = password
        self.dbname = dbname

    # Context managers
    def __enter__(self):
        ...
    def __exit__(self, exc_type, exc_val, exc_tb):
        ...

    # connect method to connect to DB
    def connect(self):
        ...

    def select_query(self):
        ...

