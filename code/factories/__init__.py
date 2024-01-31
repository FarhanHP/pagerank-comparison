"""
this package contain factory functions that instantiate certain classes that accept global arguments to eliminate of instantization of object with same global arguments repeatedly
"""

from consts import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USERNAME, DAMPING_FACTOR, IS_MULTITHREAD, MAX_WORKERS, RANDOM_WALKER_INITIAL_WALKERS_COUNT, RANDOM_WALKER_ITERATIONS
from data.db import DB
from data.domain_repository import DomainRepository
from data.page_information_repository import PageInformationRepository
from data.page_linking_repository import PageLinkingRepository
from data.page_rank_random_walkers_repository import PagerankRandomWalkersRepository
from data.page_rank_repository import PagerankRepository
from methods.dpc.cluster_separated_phi_helper import ClusterSeparatedPhiHelper
from methods.random_walker.helper_factories.graph_factory import GraphFactory
from methods.random_walker.helpers.page_informations_helper import PageInformationsHelper
from shared_helpers.p_helper import PHelper
from methods.original_pagerank.x_factory import XFactory
from methods.random_walker import RandomWalkerExecutor
from methods.random_walker.helper_factories.nodes_helper_factory import NodesHelperFactory
from shared_helpers import PageInformationsClusterizer

__db: DB | None = None

def get_db() -> DB:
  """
  get singleton global db object. If db object hasn't been instantiated or already closed, create and store new db object
  """

  global __db

  if(__db is None):
    __db = DB(DB_HOST, DB_PORT, DB_USERNAME, DB_PASSWORD, DB_NAME)

  return __db

def close_db():
  """
  close and remove singleton global db object
  """

  global __db
  
  if(__db is None):
    return
  
  __db.close()
  __db = None

def create_domain_repository() -> DomainRepository:
  return DomainRepository(get_db())

def create_page_information_repository() -> PageInformationRepository:
  return PageInformationRepository(get_db())

def create_page_rank_repository(table_name: str) -> PagerankRepository:
  return PagerankRepository(get_db(), table_name)

def create_page_linking_repository() -> PageLinkingRepository:
  return PageLinkingRepository(get_db())

def create_cluster_separated_phi_helper() -> ClusterSeparatedPhiHelper:
  return ClusterSeparatedPhiHelper(IS_MULTITHREAD, MAX_WORKERS)

def create_page_informations_clusterizer() -> PageInformationsClusterizer:
  return PageInformationsClusterizer()

def create_page_rank_random_walkers_repository() -> PagerankRandomWalkersRepository:
  return PagerankRandomWalkersRepository(get_db())

def create_x_factory() -> XFactory:
  return XFactory(IS_MULTITHREAD, MAX_WORKERS)

def create_p_helper() -> PHelper:
  return PHelper(IS_MULTITHREAD, MAX_WORKERS)

def create_nodes_helper_factory() -> NodesHelperFactory:
  return NodesHelperFactory()

def create_page_informations_helper() -> PageInformationsHelper:
  return PageInformationsHelper(create_page_information_repository(), create_page_informations_clusterizer())

def create_graph_factory() -> GraphFactory:
  return GraphFactory(DAMPING_FACTOR, create_page_linking_repository())

def create_random_walker_executor() -> RandomWalkerExecutor:
  return RandomWalkerExecutor(
    create_page_informations_helper(), 
    create_nodes_helper_factory(), 
    create_graph_factory(),
    create_p_helper(),
    RANDOM_WALKER_ITERATIONS,
    RANDOM_WALKER_INITIAL_WALKERS_COUNT,
    create_page_informations_clusterizer(),
    create_page_rank_random_walkers_repository(),
    create_domain_repository())