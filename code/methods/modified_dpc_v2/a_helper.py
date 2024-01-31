from cache import PCache
from model import PageInformation
from shared_helpers import full_matrix
from numpy.typing import NDArray
from numpy import float_
from typing import cast

class AHelper:
  """
  Helper class to create A matrix for modified dpc v2 algorithm see the skripsi for the definition
  """

  def construct_a(self, p_cache: PCache, clusters: list[list[PageInformation]]) -> NDArray[float_]:
    """
    create A matrix by merging P matrix values in PCache base on clusters

    Args:
      - p_cache: Object that can load P matrix in cache
      - clusters: page informations that are grouped by their domain forming n x Ni nested list. First level contain list of page informations that have common domain, while second level contain the page information itself

    Returns:
      n x n "A" matrix for modified DPC algorithm
    """

    domain_count = len(clusters)
    a = full_matrix((domain_count, domain_count), 0)

    for domain_source_no in range(domain_count):
      for domain_target_no in range(domain_count):
        a[domain_target_no, domain_source_no] = self.__sum_sub_transition_matrix(
          p_cache, clusters[domain_source_no], clusters[domain_target_no]
        )

      print(f"construct_a for domain {domain_source_no} done")

    return self.__normalize_a_column(a)
    
  def __sum_sub_transition_matrix(
    self, 
    p_cache: PCache, 
    cluster_source: list[PageInformation], 
    cluster_target: list[PageInformation]
  ) -> float_:
    total = 0
    source_indices = self.__get_index_from_page_informations(cluster_source)
    target_indices = self.__get_index_from_page_informations(cluster_target)

    for source_index in source_indices:
      p_column = p_cache.load_column(source_index)

      for target_index in target_indices:
        total += p_column[target_index]

    return cast(float_, total)

  def __get_index_from_page_informations(self, page_informations: list[PageInformation]) -> list[int]:
    return [page_information.index for page_information in page_informations]
  
  def __normalize_a_column(self, a: NDArray[float_]) -> NDArray[float_]:
    column_count = a.shape[1]

    for column_no in range(column_count):
      a[:, column_no] = a[:, column_no] / sum(a[:, column_no])

    return a