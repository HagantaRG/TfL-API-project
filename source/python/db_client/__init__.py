# Import 3rd-party libraries
import logging
import os
from time import sleep
from types import TracebackType
from typing import Literal, Self, overload

from psycopg import (connect, Connection)

log = logging.getLogger(__name__)

class DBClient:
    hostname: str
    port: int
    dbname: str
    user: str
    password: str
    conn_str: str

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
        """
        Enter the runtime context.
        """

        self.connection = self.connect()
        self.connected = True if self.connection else False
        return self

    @overload
    def __exit__(
            self,
            type_: type[BaseException],
            exception: BaseException,
            traceback: TracebackType,
    ) -> Literal[False]:
        ...

    @overload
    def __exit__(
            self,
            type_: None,
            exception: None,
            traceback: None,
    ) -> Literal[False]:
        ...

    def __exit__(
            self,
            type_: type[BaseException] | None = None,
            exception: BaseException | None = None,
            traceback: TracebackType | None = None,
    ) -> Literal[False]:
        """
        Exit the runtime context with the exception logged.

        :param type_: The type of exception encountered.
        :param exception: The exception object itself.
        :param traceback: The information on how the exception was reached.

        :return: Whether the exception is suppressed. ``False``, since the
            exception is only logged.
        """

        if exception is not None:
            logging.exception(exception)
        try:
            self.connection.close()
        except Exception as exception:
            logging.exception(exception)
            raise
        self.connected = False
        return False

    @property
    def connection_string(self):
        return f"host={self.hostname} port={self.port} dbname={self.dbname} user={self.user} password={self.password}"

    # connect method to connect to DB
    def connect(
        self,
        max_retry: int = 5,
        wait_time: float = 0.5,
        retry_exponent: float = 1.1
    ) -> Connection: # I'm not sure why this says this *can* return a None.
        for retries in range(max_retry + 1):
            try:
                connection: Connection = connect(conninfo=self.connection_string)
                log.info(f"Connection to {self.dbname} successful.")
                return connection
            except Exception as error:
                message: str = f"Could not connect to DB, attempting to " \
                           f"reconnect.\n{error}"
                logging.error(message)
                print(message)
                while not self._check_connection():
                    message: str = "Unable to connect to database for " \
                                   "network reasons, please check your connection/VPN."
                    print(message)
                    sleep(2)
                if retries == max_retry:
                    message: str = f"Max retries reached, raising error.\n{error}"
                    logging.error(message)
                    print(message)
                    raise ConnectionError from error
                else:
                    sleep(wait_time * (retry_exponent ** retries))

    # NB just have one method that executes *ANY* kind of query. I don't want to think about this further for now.
    def execute_query(
            self,
            query: str,
            params: list = None,
            max_retry: int = 5,
            wait_time=0.5,
            retry_exponent=1.1
    ) -> None:
        for retries in range(max_retry + 1):
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(query, params)
                    self.connection.commit()
                return
            except Exception as error:
                if retries == max_retry:
                    log.error("Max retries reached, raising error")
                    raise
                else:
                    sleep(wait_time * (retry_exponent ** retries))
                log.error(f"Encountered error in executing database query: {error}, retrying.")
                self.__exit__(type(error), error, error.__traceback__)
                self.__enter__()

    # Private methods
    def _check_connection(self) -> bool:
        """
        Check the connection to the database.

        :return: Whether the database is reachable.
        """

        command: str = f"sqlcmd -S {self.hostname} -d {self.dbname} " \
                       f"-U {self.user} -P {self.password} -q EXIT"
        result: int = os.system(command)
        return result == 0
