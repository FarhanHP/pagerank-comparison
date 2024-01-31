from numpy import float_
from cache import PCache, QListCache
from model import PageInformation
from shared_helpers import full_matrix
from numpy.typing import NDArray

class QHelper:
  """
  helper class related to Q matrix in modified dpc v2
  """

  def dump_q_list(
    self, clusters: list[list[PageInformation]], 
    p_cache: PCache, 
    q_list_cache: QListCache
  ):
    """
    for each cluster in clusters create a Q matrix and store it in cache by modifying q_list_cache

    Args:
      - clusters: page informations that are grouped by their domain forming n x Ni nested list. First level contain list of page informations that have common domain, while second level contain the page information itself
      - p_cache: object to access matrix P in cache
      - q_list_cache: object to access matrix Q in cache
    """

    print(f"dump_q_list start")

    for cluster_no in range(len(clusters)):
      self.__create_and_dump_q(q_list_cache, cluster_no, clusters[cluster_no], p_cache)

    print(f"dump_q_list done")
  
  def __create_and_dump_q(
    self, q_list_cache: QListCache,
    cluster_no: int, 
    cluster: list[PageInformation], 
    p_cache: PCache
  ):
    try:
      q = full_matrix((len(cluster), len(cluster)), 0)

      for page_no in range(len(cluster)):
        page_information = cluster[page_no]

        self.__fill_q_column(q[:, page_no], p_cache.load_column(page_information.index), cluster)

      self.__normalize_q_columns(q)

      q_list_cache.dump_q(cluster_no, q)
      print(f"dump_q_list cluster-{cluster_no} done")
    except Exception as e:
      print(f"dump_q_list: {e}")

  def __normalize_q_columns(self, q: NDArray[float_]):
    for i in range(q.shape[1]):
        q[:, i] = q[:, i]/sum(q[:, i])

  def __fill_q_column(self, pii_column: NDArray[float_], p_column: NDArray[float_], cluster: list[PageInformation]):
    try:
      for q_index, page_information in enumerate(cluster):
        pii_column[q_index] = p_column[page_information.index] 

    except Exception as e:
      print(f"fill_q_column: {e}")