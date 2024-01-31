"""
package that contain plain data class without complex logic
"""

class PageInformation():
  """
  representation of page_information table entry
  """

  index: int
  id_page: int
  url: str

  def __init__(self, index: int, id_page: int, url: str) -> None:
    self.index = index
    self.id_page = id_page
    self.url = url


class PageLinking():
  """
  representation of page_linking table entry
  """

  outgoing_link: str

  def __init__(self, outgoing_link: str) -> None:
    self.outgoing_link = outgoing_link

class Domain():
  """
  representation of domain_information table entry
  """

  domain_id: int
  url: str
  mdpcv2_rank_value: float
  dpc_rank_value: float
  random_walkers_count: int
  random_walkers_count_normalized: float

  def __init__(self, domain_id: int, url: str, mdpcv2_rank_value: float, dpc_rank_value: float, random_walkers_count: int, random_walkers_normalized: float) -> None:
    self.domain_id = domain_id
    self.url = url
    self.mdpcv2_rank_value = mdpcv2_rank_value
    self.dpc_rank_value = dpc_rank_value
    self.random_walkers_count = random_walkers_count
    self.random_walkers_count_normalized = random_walkers_normalized

class Node:
  """
  Node representation for random_walker algorithm
  """

  __page_information: PageInformation
  __walkers_count: int
  __next_walkers_count: int

  def __init__(self, page_information: PageInformation, walkers_count: int) -> None:
    self.__page_information = page_information
    self.__walkers_count = walkers_count
    self.__next_walkers_count = 0

  def clear_walkers_count(self):
    self.__walkers_count = 0

  def add_next_walkers_count(self):
    self.__next_walkers_count += 1

  def move_next_walkers_count_to_walkers_count(self):
    self.__walkers_count = self.__next_walkers_count
    self.__next_walkers_count = 0

  def get_walkers_count(self):
    return self.__walkers_count
  
  def get_next_walkers_count(self):
    return self.__next_walkers_count
  
  def get_page_information(self):
    """get copy of PageInformation which this node has"""

    return PageInformation(self.__page_information.index, self.__page_information.id_page, self.__page_information.url)
  
  def get_page_information_index(self) -> int:
    """get index of page_information that has been sorted by its cluster"""

    return self.__page_information.index