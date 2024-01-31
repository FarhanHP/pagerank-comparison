from model import PageInformation, Node
from data.page_information_repository import PageInformationRepository
from shared_helpers import PageInformationsClusterizer, sort_page_information_by_domain


class PageInformationsHelper:
  """
  helper class managing all page informations in this program from page_information table in database

  sort the list base on their domains, and set page_information.index base on the index in the list

  Properties
    - page_informations: N-length list of page informations
  """

  __page_informations: list[PageInformation]

  def __init__(self, page_information_repository: PageInformationRepository, page_information_clusterizer: PageInformationsClusterizer) -> None:
    page_informations = page_information_repository.get_all_page_informations()
    clusters = page_information_clusterizer.clusterize(page_informations)
    self.__page_informations = sort_page_information_by_domain(clusters)

  def create_nodes(self, initial_walkers_count: int) -> list[Node]:
    """
    for each page information create a node with node.walkers_count = initial_walkers_count

    Args:
      - initial_walkers_count

    Returns:
      N-length list of nodes
    """

    return [Node(page_information, initial_walkers_count) for page_information in self.__page_informations]
  
  def get_page_informations(self) -> list[PageInformation]:
    """
    get all page informations
    """

    return self.__page_informations