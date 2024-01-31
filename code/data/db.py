from mysql.connector import connect, CMySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.connection import MySQLConnection
from typing import Union

DB_Connection = Union[PooledMySQLConnection, MySQLConnection, CMySQLConnection]

class DB:
  """wrapper class for mysql db connection"""

  __host: str
  __port: str
  __username: str
  __password: str
  __db_name: str
  __db_conn: DB_Connection

  def __init__(self, host: str, port: str, username: str, password: str, db_name: str) -> None:
    self.__host = host
    self.__port = port
    self.__username = username
    self.__password = password
    self.__db_name = db_name
    self.__db_conn = self.construct_db_conn()

  def construct_db_conn(self) -> DB_Connection:
    """
    create and get new db connection
    """

    return connect(host=self.__host, port=self.__port, user=self.__username, password=self.__password, database=self.__db_name)
  
  def get_db_conn(self) -> DB_Connection:
    """
    get existing db connection
    """

    return self.__db_conn

  def close(self):
    """
    close db connection
    """

    self.__db_conn.close()