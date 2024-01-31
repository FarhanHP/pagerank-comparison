from typing import cast
from data.db import DB
from model import Domain

class DomainRepository:
  """
  Intermediary for CRUD domain_rank table in database
  """
  
  __db: DB
  __table_name = "domain_information"

  def __init__(self, db: DB) -> None:
    self.__db = db

  def get_all_domains(self) -> list[Domain]:
    """
    get all domain_rank entries
    """

    query = f"SELECT * FROM {self.__table_name}"
    db_conn = self.__db.get_db_conn()
    cursor = db_conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    return [Domain(cast(int, row[0]), cast(str, row[1]), cast(float, row[2]), cast(float, row[3]), cast(int, row[4]), cast(float, row[5])) for row in rows]

  def insert_domains(self, domain_ids: list[int], urls: list[str]):
    """
    insert new domain_rank entries, if new entries have same id with existing entries, replace with newer entries
    """

    if(len(domain_ids) != len(urls)):
      raise Exception()
    
    db_conn = self.__db.get_db_conn()
    cursor = db_conn.cursor()

    query = f"INSERT INTO {self.__table_name} (domain_id, url) VALUES (%s, %s) ON DUPLICATE KEY UPDATE url=VALUES(url)"
    query_values: list[tuple[int, str]] = []

    for i in range(len(domain_ids)):
      query_values.append((domain_ids[i], urls[i]))

    cursor.executemany(query, query_values)
    db_conn.commit()
    cursor.close()

  def update_mdpcv2_rank(self, domain_urls: list[str], rank_values: list[float]):
    self.__update_domain_rank("mdpcv2_rank_value", domain_urls, rank_values)

  def update_dpc_rank(self, domain_urls: list[str], rank_values: list[float]):
    self.__update_domain_rank("dpc_rank_value", domain_urls, rank_values)

  def update_domain_walkers_count(self, domain_urls: list[str], walkers_counts: list[int]):
    self.__update_domain_rank("random_walkers_count", domain_urls, walkers_counts)

  def update_domain_walkers_normalized(self, domain_urls: list[str], walker_values: list[float]):
    self.__update_domain_rank("random_walkers_count_normalized", domain_urls, walker_values)

  def __update_domain_rank(self, rank_field_name: str, domain_urls: list[str], rank_values: list):
    """
    update rank value base on rank_field_name
    available field names = mdpcv2_rank_value, dpc_rank_value, random_walkers_count, random_walkers_count_normalized
    """

    if(len(domain_urls) != len(rank_values)):
      raise Exception()
    
    db_conn = self.__db.get_db_conn()
    cursor = db_conn.cursor()

    query = f"UPDATE {self.__table_name} SET {rank_field_name}=%s WHERE url=%s"
    query_values: list[tuple[float, str]] = []

    for i in range(len(domain_urls)):
      query_values.append((rank_values[i], domain_urls[i]))

    cursor.executemany(query, query_values)
    db_conn.commit()
    cursor.close()