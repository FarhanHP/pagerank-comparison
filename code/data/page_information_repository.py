from typing import cast
from data.db import DB, DB_Connection
from model import PageInformation
from mysql.connector.types import RowType


class PageInformationRepository:
  """
  Intermediary for CRUD page_information table in database
  """

  __db: DB
  __table_name = "page_information"

  def __init__(self, db: DB) -> None:
    self.__db = db

  def get_all_page_informations(self, use_existing_db_conn = True) -> list[PageInformation]:
    """
    get all page_information entries
    """

    db_conn = self.__db.get_db_conn() if(use_existing_db_conn) else self.__db.construct_db_conn()
    page_informations = self.__get_all_page_informations_from_db_conn(db_conn)
    output = []

    if(not use_existing_db_conn):
      db_conn.close()

    for page_information in page_informations:
      output.append(PageInformation(0, cast(int, page_information[0]), cast(str, page_information[1])))

    return output
  
  def __get_all_page_informations_from_db_conn(
    self, 
    db_conn: DB_Connection
  ) -> list[RowType]:
    cursor = db_conn.cursor()
    cursor.execute(f"SELECT id_page, url FROM {self.__table_name}")
    output = cursor.fetchall()
    cursor.close()
    return output
  
  def get_page_information_by_id(self, page_information_id: int) -> PageInformation:
    """
    get a page_information entry with matched id, raise exception if not exist
    """

    db_conn = self.__db.get_db_conn()
    cursor = db_conn.cursor()
    cursor.execute(f"SELECT id_page, url FROM {self.__table_name} WHERE id_page={page_information_id}")
    query_result = cursor.fetchone()

    if(query_result is None):
      raise Exception("page_information_id not exist")
    
    return PageInformation(0, cast(int, query_result[0]), cast(str, query_result[1]))
  
  def update_backlink_count_by_page_ids(self, page_ids: list[int], backlink_counts: list[int]):
    """
    update backlink_count value of page_information entries with matching page_ids argument respectively
    """

    if(len(page_ids) != len(backlink_counts)):
      raise Exception("page_ids and backlink_counts must have same length")
    
    db_conn = self.__db.get_db_conn()
    cursor = db_conn.cursor()
    query = f"UPDATE {self.__table_name} SET backlink_count=%s WHERE id_page=%s"
    query_values: list[tuple[int, int]] = []

    for i in range(len(page_ids)):
      query_values.append((backlink_counts[i], page_ids[i]))

    cursor.executemany(query, query_values)
    db_conn.commit()
    cursor.close()

  def update_domain_id_by_page_ids(self, page_ids: list[int], domain_ids: list[int]):
    """
    update domain_id value of page_information entries with matching page_ids argument respectively
    """

    if(len(page_ids) != len(domain_ids)):
      raise Exception()
    
    db_conn = self.__db.get_db_conn()
    cursor = db_conn.cursor()
    query = f"UPDATE {self.__table_name} SET domain_id=%s WHERE id_page=%s"
    query_values: list[tuple[int, int]] = []

    for i in range(len(page_ids)):
      query_values.append((domain_ids[i], page_ids[i]))

    cursor.executemany(query, query_values)
    db_conn.commit()
    cursor.close()

  def update_backlink_count_by_page_id(self, page_id: int, backlink_count: int):
    """
    update backlink_count value of page_information entries with matching page_ids argument respectively
    """

    db_conn = self.__db.get_db_conn()
    cursor = db_conn.cursor()

    query = f"UPDATE {self.__table_name} SET backlink_count={backlink_count} WHERE id_page={page_id}"
    cursor.execute(query)
    db_conn.commit()

    cursor.close()
    