from typing import cast
from data.db import DB
from model import Node


class PagerankRandomWalkersRepository:
  """
  Intermediary for CRUD page_rank_random_walkers table in database
  """

  __db: DB
  __table_name = "page_rank_random_walkers"

  def __init__(self, db: DB) -> None:
    self.__db = db

  def insert_ranks(self, nodes: list[Node]):
    """
    Insert new entries base on node.page_information and node.walkers_count
    """

    db_conn = self.__db.get_db_conn()
    cursor = db_conn.cursor()

    query = f"INSERT INTO {self.__table_name} (id, page_information_id, walkers_count) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE walkers_count = VALUES(walkers_count)"
    
    query_values: list[tuple[int, int, int]] = []
    for node in nodes:
      page_id = node.get_page_information().id_page
      walkers_count = node.get_walkers_count()
      query_values.append((page_id, page_id, walkers_count))

    cursor.executemany(query, query_values)
    db_conn.commit()

    cursor.close()

  def get_page_ids_sorted_by_rank(self) -> list[int]:
    """
    Get page_information_ids of the table entries sorted by walkers_count descending. If entries have same walkers_count, sorted those entries base on its page_information_id ascendingly
    """

    db_conn = self.__db.get_db_conn()
    cursor = db_conn.cursor()
    query = f"SELECT page_information_id FROM {self.__table_name} ORDER BY walkers_count DESC, page_information_id ASC"
    cursor.execute(query)
    query_result = cursor.fetchall()
    cursor.close()

    return [cast(int, row[0]) for row in query_result]
  
  def get_page_ids_and_walkers_sorted_by_rank(self) -> list[tuple[int, int]]:
    """
    Get page_information_ids and walkers_counts of the table entries sorted by walkers_count descending. If entries have same walkers_count, sorted those entries base on its page_information_id ascendingly
    """

    db_conn = self.__db.get_db_conn()
    cursor = db_conn.cursor()
    query = f"SELECT page_information_id, walkers_count FROM {self.__table_name} ORDER BY walkers_count DESC, page_information_id ASC"
    cursor.execute(query)
    query_result = cursor.fetchall()
    cursor.close()

    return [(cast(int, row[0]), cast(int, row[1])) for row in query_result]
  
  def get_page_id_and_walkers_count_sorted_by_page_id(self) -> list[tuple[int, int]]:
    """
    Get page_information_ids and walkers_counts of the table entries sorted by page_information_id ascending
    """

    db_conn = self.__db.get_db_conn()
    cursor = db_conn.cursor()
    query = f"SELECT page_information_id, walkers_count FROM {self.__table_name} ORDER BY page_information_id ASC"
    cursor.execute(query)
    query_result = cursor.fetchall()
    cursor.close()

    return [(cast(int, row[0]), cast(int, row[1])) for row in query_result]
