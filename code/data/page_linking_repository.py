from typing import Optional, cast
from data.db import DB, DB_Connection
from model import PageLinking
from mysql.connector.types import RowType


class PageLinkingRepository:
  """
  Intermediary for CRUD page_linking table in database
  """

  __db: DB
  __table_name = "page_linking"

  def __init__(self, db: DB) -> None:
    self.__db = db

  def get_page_linkings_by_page_id(self, page_id: int, use_existing_db_conn: Optional[bool]  = True) -> list[PageLinking]:
    """
    get all page_linking entries with matching page_id. use_existing_db_conn = False will create new disposable DB connection, use this when accessing DB simultaneously in multithread. The disposable DB connection will be closed after the method operation finised
    """

    db_conn = self.__get_db_conn(use_existing_db_conn)
    page_linkings = self.__get_page_linkings_by_page_id_from_db_conn(db_conn, page_id)
    output = []

    if(not use_existing_db_conn):
      db_conn.close()
    
    for page_linking in page_linkings:
      output.append(PageLinking(cast(str, page_linking[0])))

    return output
  
  def __get_page_linkings_by_page_id_from_db_conn(self, db_conn: DB_Connection, page_id: int) -> list[RowType]:
    cursor = db_conn.cursor()
    # "BINARY" keyword for case sensitive comparison
    cursor.execute(f"SELECT DISTINCT outgoing_link FROM {self.__table_name} WHERE page_id={page_id} AND outgoing_link IN (SELECT BINARY url FROM page_information)")
    output = cursor.fetchall()
    cursor.close()
    return output
  
  def get_page_linkings_count_by_page_id(self, page_id: int, use_existing_db_conn: Optional[bool] = True) -> int:
    """
    get all page_linking entries count with matching page_id. use_existing_db_conn = False will create new disposable DB connection, use this when accessing DB simultaneously in multithread. The disposable DB connection will be closed after the method operation finised
    """

    db_conn = self.__get_db_conn(use_existing_db_conn)
    
    cursor = db_conn.cursor()
    # "BINARY" keyword for case sensitive comparison
    cursor.execute(f"SELECT COUNT(DISTINCT outgoing_link) FROM {self.__table_name} WHERE page_id={page_id} AND outgoing_link IN (SELECT BINARY url FROM page_information)")
    output = cast(RowType, cursor.fetchone())[0]
    cursor.close()

    if(not use_existing_db_conn):
      db_conn.close()

    return cast(int, output)
  
  def is_page_linking_exist(self, page_id: int, outgoing_link: str, use_existing_db_conn: Optional[bool] = True) -> bool:
    """
    Return true if a page_linking entry with matching page_id and outgoing_link exist. use_existing_db_conn = False will create new disposable DB connection, use this when accessing DB simultaneously in multithread. The disposable DB connection will be closed after the method operation finised
    """

    db_conn = self.__get_db_conn(use_existing_db_conn)
    
    cursor = db_conn.cursor()
    # "BINARY" keyword for case sensitive comparison
    cursor.execute(f"SELECT COUNT(*) FROM {self.__table_name} WHERE page_id={page_id} AND outgoing_link={outgoing_link}")
    count = cast(int, cast(RowType, cursor.fetchone())[0])
    cursor.close()

    if(not use_existing_db_conn):
      db_conn.close()

    return count > 0
  
  def get_back_linking_count_by_outgoing_url(self, url: str) -> int:
    """
    Get backlinking (a link that point to the url or has matching outgoing_url with the url) count of the url. use_existing_db_conn = False will create new disposable DB connection, use this when accessing DB simultaneously in multithread. The disposable DB connection will be closed after the method operation finised
    """

    db_conn = self.__get_db_conn()

    cursor = db_conn.cursor()
    query = f"SELECT COUNT(DISTINCT page_id) FROM {self.__table_name} WHERE outgoing_link='{url}'"
    cursor.execute(query)
    query_result = cursor.fetchone()

    if(query_result is None):
      return 0
    
    return cast(int, query_result[0])

  def __get_db_conn(self, use_existing_db_conn: Optional[bool] = True) -> DB_Connection:
    return self.__db.get_db_conn() if(use_existing_db_conn) else self.__db.construct_db_conn()
