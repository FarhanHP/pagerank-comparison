from data.db import DB
from model import PageInformation
from numpy.typing import NDArray
from numpy import float_
from typing import cast


class PagerankRepository:
  """
  Intermediary for CRUD page_rank_dpc, page_rank_modified_dpc_v2, page_rank_original_pagerank, page_rank_original_pagerank_dpc_paper_version tables in database
  """

  __db: DB
  __table_name: str

  def __init__(self, db: DB, table_name: str) -> None:
    self.__db = db
    self.__table_name = table_name

  def insert_ranks(self, page_informations: list[PageInformation], pagerank_vector: NDArray[float_]):
    """
    Insert rank values base on the N-length page_informations and N-x-1-shape pagerank_vector respectively.
    """

    if(not self.__is_has_same_length(page_informations, pagerank_vector)):
      return
    
    self.__execute_insert_ranks(page_informations, pagerank_vector)
    
  def __execute_insert_ranks(self, page_informations: list[PageInformation], pagerank_vector: NDArray[float_]):
    db_conn = self.__db.get_db_conn()
    cursor = db_conn.cursor()
    query = f"INSERT INTO {self.__table_name} (id, page_information_id, value) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE value = VALUES(value)"
    values = self.__map_to_query_values(page_informations, pagerank_vector)
    cursor.executemany(query, values)
    db_conn.commit()
    cursor.close()

  def __map_to_query_values(self, page_informations: list[PageInformation], pagerank_vector: NDArray[float_]) -> list[tuple[str, str, str]]:
    values: list[tuple[str, str, str]] = [("", "", "")] * (self.__get_max_page_information_id(page_informations) + 1)

    for page_information in page_informations:
      values[page_information.id_page] = (str(page_information.id_page), str(page_information.id_page), str(pagerank_vector[page_information.index]))

    values = self.__clean_query_values(values)

    return values
  
  def __get_max_page_information_id(self, page_informations: list[PageInformation]) -> int:
    max_page_information_id = -1
    for page_information in page_informations:
      if(page_information.id_page > max_page_information_id):
        max_page_information_id = page_information.id_page

    return max_page_information_id
  
  def __clean_query_values(self, query_values: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    for index, query_value in enumerate(query_values):
      if(query_value[0] == ""):
        del query_values[index]

    return query_values

  def __is_has_same_length(self, lst: list, vector: NDArray) -> bool:
    return len(lst) == vector.shape[0]
  
  def get_page_ids_sorted_by_rank(self) -> list[int]:
    """
    Get page_information_ids of the table entries sorted by value descending. If entries have same value, sorted those entries base on its page_information_id ascendingly
    """

    db_conn = self.__db.get_db_conn()
    cursor = db_conn.cursor()
    query = f"SELECT page_information_id FROM {self.__table_name} ORDER BY value DESC, page_information_id ASC"
    cursor.execute(query)
    query_result = cursor.fetchall()
    cursor.close()
    return [cast(int, row[0]) for row in query_result]
  
  def get_page_ids_and_rank_value(self) -> list[tuple[int, float]]:
    """
    Get page_information_ids and values of the table entries sorted by value descending. If entries have same value, sorted those entries base on its page_information_id ascendingly
    """

    db_conn = self.__db.get_db_conn()
    cursor = db_conn.cursor()
    query = f"SELECT page_information_id, value FROM {self.__table_name} ORDER BY value DESC, page_information_id ASC"
    cursor.execute(query)
    query_result = cursor.fetchall()
    cursor.close()
    return [(cast(int, row[0]), cast(float, row[1])) for row in query_result]
  
  def get_page_id_and_rank_value_sorted_by_page_id(self) -> list[tuple[int, float]]:
    """
    Get page_information_ids and values of the table entries sorted by page_information_id ascending.
    """

    db_conn = self.__db.get_db_conn()
    cursor = db_conn.cursor()
    query = f"SELECT page_information_id, value FROM {self.__table_name} ORDER BY page_information_id ASC"
    cursor.execute(query)
    query_result = cursor.fetchall()
    cursor.close()
    return [(cast(int, row[0]), cast(float, row[1])) for row in query_result]
  