from model import PageInformation
from cache import PCache, QListCache, PiiListCache
from numpy import float_
from numpy.typing import NDArray
from shared_helpers import full_matrix
import threading

class PartitionedPHelper:
  def dump_partitioned_p(
    self, clusters: list[list[PageInformation]], p_cache: PCache, 
    q_list_cache: QListCache, pii_list_cache: PiiListCache
  ):
    """
    partitioning N x N P matrix into Ni x Ni Pii matrix and normalized Pii matrix as Ni x Ni Qi matrix. Dump it into cache using q_list_cache and pii_list_cache

    Args:
      - clusters: page informations that are grouped by their domain forming n x Ni nested list. First level contain list of page informations that have common domain, while second level contain the page information itself
      - p_cache: object to access matrix P in cache
      - q_list_cache: object to write Qi matrix into cache
      - pii_list_cache: object to write Pii matrix into cache
    """

    print(f"dump_partitioned_p start")

    for cluster_no in range(len(clusters)):
      self.__create_and_dump_pii_and_q(q_list_cache, pii_list_cache, cluster_no, clusters[cluster_no], p_cache)

    print(f"dump_partitioned_p done")
  
  def __create_and_dump_pii_and_q(
    self, q_list_cache: QListCache, pii_list_cache: PiiListCache, 
    cluster_no: int, cluster: list[PageInformation], p_cache: PCache
  ):
    try:
      pii = full_matrix((len(cluster), len(cluster)), 0)

      for page_no in range(len(cluster)):
        page_information = cluster[page_no]

        self.__fill_pii_column(pii[:, page_no], p_cache.load_column(page_information.index), cluster)

      pii_list_cache.dump_pii(cluster_no, pii)

      # convert pii to q by normalize its columns
      for i in range(pii.shape[1]):
        pii[:, i] = pii[:, i]/sum(pii[:, i])

      q_list_cache.dump_q(cluster_no, pii)
      print(f"dump_partitioned_p cluster-{cluster_no} done; thread_id={threading.get_native_id()}")
    except Exception as e:
      print(f"dump_partitioned_p: {e}")

  def __fill_pii_column(self, pii_column: NDArray[float_], p_column: NDArray[float_], cluster: list[PageInformation]):
    try:
      for q_index, page_information in enumerate(cluster):
        pii_column[q_index] = p_column[page_information.index]

    except Exception as e:
      print(f"fill_pii_column: {e}")
