from data.page_rank_random_walkers_repository import PagerankRandomWalkersRepository
from data.domain_repository import DomainRepository
from methods.random_walker.helper_factories.graph_factory import GraphFactory
from methods.random_walker.helper_factories.nodes_helper_factory import NodesHelperFactory
from methods.random_walker.helpers.page_informations_helper import PageInformationsHelper
from model import Node
from shared_helpers import PageInformationsClusterizer, show_and_reset_smallest_and_highest_memory_usage
from shared_helpers.p_helper import PHelper
import random

class RandomWalkerExecutor:
  """
  executor for random walker algorithm

  Args:
    - page_informations_helper: helper class to manage list of page informations
    - nodes_helper_factory: factory class to construct nodes helper
    - graph_factory: factory class to construct graph helper class
    - random_walker_iterations: maximum iterations for random walker program
    - initial_walkers_count: initial walkers count for each node
    - page_informations_clusterizer: helper class to clusterize page informations
    - page_rank_walkers_repository: class to store random walkers output into database
    - domain_repository: class to store random walkers output for each page information domain
  """

  __page_informations_helper: PageInformationsHelper
  __nodes_helper_factory: NodesHelperFactory
  __graph_factory: GraphFactory
  __p_helper: PHelper
  __random_walker_iterations: int
  __initial_walkers_count: int
  __page_informations_clusterizer: PageInformationsClusterizer
  __page_rank_random_walkers_repository: PagerankRandomWalkersRepository | None
  __domain_repository: DomainRepository | None

  def __init__(
    self, 
    page_informations_helper: PageInformationsHelper, 
    nodes_helper_factory: NodesHelperFactory,
    graph_factory: GraphFactory,
    p_helper: PHelper,
    random_walker_iterations: int,
    initial_walkers_count: int,
    page_informations_clusterizer: PageInformationsClusterizer,
    page_rank_random_walkers_repository: PagerankRandomWalkersRepository | None = None,
    domain_repository: DomainRepository | None = None
  ) -> None:
    self.__page_informations_helper = page_informations_helper
    self.__nodes_helper_factory = nodes_helper_factory
    self.__random_walker_iterations = random_walker_iterations
    self.__initial_walkers_count = initial_walkers_count
    self.__page_informations_clusterizer = page_informations_clusterizer
    self.__p_helper = p_helper
    self.__graph_factory = graph_factory
    self.__page_rank_random_walkers_repository = page_rank_random_walkers_repository
    self.__domain_repository = domain_repository

  def execute(self):
    """
    main entry point for random walker algorithm
    """
    nodes = self.__page_informations_helper.create_nodes(self.__initial_walkers_count)
    nodes_helper = self.__nodes_helper_factory.create_helper(nodes)
    graph = self.__graph_factory.create_helper(self.__p_helper, nodes_helper, self.__page_informations_helper)
    
    for i in range(self.__random_walker_iterations):
      for current_node in nodes:
        destination_nodes_and_probabilites = graph.get_destination_nodes_and_probabilites(current_node)
        walkers_count = current_node.get_walkers_count()
        choosen_nodes = random.choices(destination_nodes_and_probabilites[0], weights=destination_nodes_and_probabilites[1], k=walkers_count)
        choosen_nodes_helper = self.__nodes_helper_factory.create_helper(choosen_nodes)
        choosen_nodes_helper.add_next_walkers_count()
        current_node.clear_walkers_count()
        show_and_reset_smallest_and_highest_memory_usage(f"iteration-{i} for page index {current_node.get_page_information_index()} done")

      nodes_helper.move_nodes_next_walkers_count_to_walkers_count()

    self.__update_domain_walkers_count(nodes)
    self.__insert_ranks(nodes)
  
  def __update_domain_walkers_count(self, nodes: list[Node]):
    if(self.__domain_repository is None):
      return

    domain_dict: dict[str, int] = {}

    for node in nodes:
      domain_url = self.__page_informations_clusterizer.get_domain(node.get_page_information())
      if(domain_url in domain_dict.keys()):
        domain_dict[domain_url] += node.get_walkers_count()
      else:
        domain_dict[domain_url] = node.get_walkers_count()

    domain_urls = list(domain_dict.keys())
    walkers_counts = [domain_dict[domain_url] for domain_url in domain_urls]
    self.__domain_repository.update_domain_walkers_count(domain_urls, walkers_counts)

  def __insert_ranks(self, nodes: list[Node]):
    if(self.__page_rank_random_walkers_repository is None):
      return
    
    self.__page_rank_random_walkers_repository.insert_ranks(nodes)

