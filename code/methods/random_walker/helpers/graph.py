from shared_helpers.p_helper import PHelper
from methods.random_walker.helpers.nodes_helper import NodesHelper
from methods.random_walker.helpers.page_informations_helper import PageInformationsHelper
from data.page_linking_repository import PageLinkingRepository
from model import Node
from numpy.typing import NDArray
from numpy import float_
from typing import cast

class Graph:
  """
  Properties:
    - p_helper: helper class to create P matrix
    - nodes_helper: helper class to manage list of nodes
    - page_linking_repository: repository class to access page_linking entries in database
    - d: damping factor
    - p: P transition matrix 
  """
  __nodes_helper: NodesHelper
  __page_linking_repository: PageLinkingRepository
  __d: float
  __p: NDArray[float_]

  def __init__(self, d: float, page_linking_repository: PageLinkingRepository):
    self.__d = d
    self.__page_linking_repository = page_linking_repository

  def insert_stateful_params(self, p_helper: PHelper, nodes_helper: NodesHelper, page_informations_helper: PageInformationsHelper):
    """
    method to insert parameters that are stateful. Stateful means for every instances will have different mutable object params

    Args:
      - p_helper: helper class to create P matrix
      - nodes_helper: helper class to manage list of nodes
      - page_informations_helper: helper class managing list of page informations
    """

    self.__nodes_helper = nodes_helper
    self.__p = p_helper.create_p(self.__d, page_informations_helper.get_page_informations(), self.__page_linking_repository.get_page_linkings_by_page_id)

  def get_destination_nodes_and_probabilites(self, source_node: Node) -> tuple[list[Node], list[float]]:
    """get N-length list of destination nodes and their N-length list of probabilites respectively from source_node"""

    probabilites = self.__p[:, source_node.get_page_information().index]

    return (self.__nodes_helper.get_nodes(True), cast(list[float], list(probabilites)))