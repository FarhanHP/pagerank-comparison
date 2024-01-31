from methods.random_walker.helpers.nodes_helper import NodesHelper
from model import Node


class NodesHelperFactory:
  def create_helper(self, nodes: list[Node]) -> NodesHelper:
    nodes_helper = NodesHelper()
    nodes_helper.insert_stateful_fields(nodes)
    return nodes_helper