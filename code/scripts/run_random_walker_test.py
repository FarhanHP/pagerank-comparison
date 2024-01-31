import os
import sys

sys.path.append(os.path.abspath(os.path.join('')))

from model import PageInformation, PageLinking
import tracemalloc
from methods.random_walker import RandomWalkerExecutor
from factories import create_page_informations_clusterizer, create_nodes_helper_factory, get_db, create_p_helper
from data.page_information_repository import PageInformationRepository
from data.db import DB
from data.page_linking_repository import PageLinkingRepository
from typing import cast
from methods.random_walker.helper_factories.graph_factory import GraphFactory
from consts import DAMPING_FACTOR
from methods.random_walker.helpers.page_informations_helper import PageInformationsHelper



class PageInformationRepositoryForTest(PageInformationRepository):
  __page_informations_count_limit: int
  __db: DB
  __page_informations: list[PageInformation] | None = None

  def __init__(self, db: DB, limit: int):
    self.__page_informations_count_limit = limit
    self.__db = db

  def get_all_page_informations(self) -> list[PageInformation]:
    if(self.__page_informations is None):
      self.__fetch_all_page_informations_from_db()

    return cast(list[PageInformation], self.__page_informations)
    
  def __fetch_all_page_informations_from_db(self):
    db_conn = self.__db.get_db_conn()
    cursor = db_conn.cursor()
    cursor.execute(f"SELECT id_page, url FROM page_information LIMIT {self.__page_informations_count_limit}")
    page_informations = cursor.fetchall()
    cursor.close()

    output = []

    for page_information in page_informations:
      output.append(PageInformation(0, cast(int, page_information[0]), cast(str, page_information[1])))

    self.__page_informations = output
  
class PageLinkingRepositoryForTest(PageLinkingRepository):
  __db: DB
  __page_informations: list[PageInformation]
  __page_informations_url: list[str] | None = None

  def __init__(self, db: DB, page_informations: list[PageInformation]) -> None:
    self.__db = db
    self.__page_informations = page_informations

  def get_page_linkings_by_page_id(self, page_id: int) -> list[PageLinking]:
    db_conn = self.__db.get_db_conn()
    cursor = db_conn.cursor()
    # "BINARY" keyword for case sensitive comparison
    cursor.execute(f"SELECT DISTINCT outgoing_link FROM page_linking WHERE page_id={page_id} AND CAST(outgoing_link AS BINARY) IN {tuple(self.__get_page_informations_url())}")
    page_linkings = cursor.fetchall()
    cursor.close()

    output = []
    for page_linking in page_linkings:
      output.append(PageLinking(cast(str, page_linking[0])))

    return output
  
  def __get_page_informations_url(self) -> list[str]:
    if(self.__page_informations_url is None):
      self.__page_informations_url = [page_information.url for page_information in self.__page_informations]

    return self.__page_informations_url

def main():
  tracemalloc.start()

  page_information_repository = PageInformationRepositoryForTest(get_db(), 30000)
  page_linking_repository = PageLinkingRepositoryForTest(get_db(), page_information_repository.get_all_page_informations())
  graph_factory = GraphFactory(DAMPING_FACTOR, page_linking_repository)

  random_walker_executor = RandomWalkerExecutor(
    PageInformationsHelper(page_information_repository, create_page_informations_clusterizer()),
    create_nodes_helper_factory(),
    graph_factory,
    create_p_helper(),
    10,
    100,
    create_page_informations_clusterizer()
  )
  random_walker_executor.execute()

  traced_memory = tracemalloc.get_traced_memory()

  print(f"smallest memory usage: {traced_memory[0]} Bytes")
  print(f"highest memory usage: {traced_memory[1]} Bytes")

  tracemalloc.stop()

if(__name__ == "__main__"):
  main()