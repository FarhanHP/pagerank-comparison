from model import Node

class NodesHelper:
  """
  helper class managing list of nodes

  Properties
    - sorted: true if nodes already sorted base on its page_information.index
    - nodes: N-length list of nodes
  """

  __sorted = False
  __nodes: list[Node]

  def insert_stateful_fields(self, nodes: list[Node]):
    """
    method to insert parameters that are stateful. Stateful means for every instances will have different mutable object params

    Args:
      - nodes: N-length list of nodes
    """

    self.__nodes = nodes

  def get_nodes(self, sorted: bool = False) -> list[Node]:
    """
    get all nodes
    
    Args:
      - sorted: default False, set True will sort nodes by its page_information.index before return the nodes
    """

    if(sorted and not self.__sorted): # only sort nodes once
      self.__sort_nodes_by_page_information_index()

    return self.__nodes
  
  def __sort_nodes_by_page_information_index(self):
    self.__nodes.sort(key = lambda node: node.get_page_information_index())
    self.__sorted = True
  
  def move_nodes_next_walkers_count_to_walkers_count(self):
    """
    for each node set node.walkers_count = node.next_walkers_count then set node.next_walkers_count = 0
    """

    for node in self.__nodes:
      node.move_next_walkers_count_to_walkers_count()

  def add_next_walkers_count(self):
    """
    for each node increment node.walkers_count
    """

    for node in self.__nodes:
      node.add_next_walkers_count()