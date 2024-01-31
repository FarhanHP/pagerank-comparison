from data.page_linking_repository import PageLinkingRepository
from methods.random_walker.helpers.page_informations_helper import PageInformationsHelper
from methods.random_walker.helpers.graph import Graph
from methods.random_walker.helpers.nodes_helper import NodesHelper
from shared_helpers.p_helper import PHelper

class GraphFactory:
  __damping_factor: float
  __page_linking_repository: PageLinkingRepository

  def __init__(self, damping_factor: float, page_linking_repository: PageLinkingRepository) -> None:
    self.__damping_factor = damping_factor
    self.__page_linking_repository = page_linking_repository

  def create_helper(self, p_helper: PHelper, nodes_helper: NodesHelper, page_informations_helper: PageInformationsHelper) -> Graph:
    graph = Graph(self.__damping_factor, self.__page_linking_repository)
    graph.insert_stateful_params(p_helper, nodes_helper, page_informations_helper)
    return graph