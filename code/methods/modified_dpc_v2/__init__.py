"""
package for modified dpc v2 algorithm program. Origin of "v2" of the algorithm name due to existence of first modified dpc algorithm, but scrapped due to certain reasons.
"""

from cache import PCache, QListCache
from data.domain_repository import DomainRepository
from methods.dpc.cluster_separated_phi_helper import ClusterSeparatedPhiHelper
from methods.modified_dpc_v2.q_helper import QHelper
from methods.modified_dpc_v2.a_helper import AHelper
from model import PageInformation
from shared_helpers import full_matrix, show_and_reset_smallest_and_highest_memory_usage
from numpy.typing import NDArray
from numpy import float_
from methods.dpc import pagerank_dpc

class ModifiedDPCV2Executor:
  """
  Class that contain core logic of modified DPC v2 algorithm (or refered as modified dpc in this research report/"skripsi")
  """

  __p_cache: PCache
  __q_list_cache: QListCache

  __q_helper: QHelper
  __cluster_separated_phi_helper: ClusterSeparatedPhiHelper
  __a_helper: AHelper

  __domain_repository: DomainRepository

  def insert_caches(
    self,
    p_cache: PCache,
    q_list_cache: QListCache
  ):
    """
    Insert cache classes that will be used later
    """

    self.__p_cache = p_cache
    self.__q_list_cache = q_list_cache

  def insert_helpers(
    self,
    q_helper: QHelper,
    cluster_separated_phi_helper: ClusterSeparatedPhiHelper,
    a_helper: AHelper,
  ):
    """
    Insert helper classes that will be used later
    """

    self.__q_helper = q_helper
    self.__cluster_separated_phi_helper = cluster_separated_phi_helper
    self.__a_helper = a_helper

  def insert_repositories(self, domain_repository: DomainRepository):
    """
    Insert repository classes that will be used later
    """

    self.__domain_repository = domain_repository

  def execute(
    self,
    clusters: dict[str, list[PageInformation]], 
    epsilon: float,
    pagerank_dpc_max_iteration: int,
    start_time: float
  )-> NDArray[float_]:
    """
    Entry point to start mdofied dpc v2 program

    Args:
      - clusters: page informations that are grouped by their domain forming python dictionary.
        - key: domain url
        - value: list of page information that belong to the domain
      - epsilon: maximum l1 norm difference/delta between pagerank vector current iteration
      - pagerank_dpc_max_iteration: max iteration for pagerank iterations
      - start_time: start time when this method is called in seconds

    Returns:
      - N x 1 pagerank vector
    """

    cluster_page_informations = list(clusters.values())

    self.__q_helper.dump_q_list(
      cluster_page_informations,
      self.__p_cache,
      self.__q_list_cache,
    )

    show_and_reset_smallest_and_highest_memory_usage("create and dump matrix Qs step", start_time)

    cluster_separated_phi = self.__cluster_separated_phi_helper.construct_cluster_separated_phi(
      cluster_page_informations,
      self.__q_list_cache,
      pagerank_dpc,
      epsilon,
      pagerank_dpc_max_iteration
    )

    show_and_reset_smallest_and_highest_memory_usage("cluster_separated_phi step", start_time)

    a = self.__a_helper.construct_a(self.__p_cache, cluster_page_informations)

    show_and_reset_smallest_and_highest_memory_usage("matrix a step", start_time)

    z = pagerank_dpc(full_matrix(a.shape[0], 1/len(clusters)), a, epsilon, pagerank_dpc_max_iteration, "pagerank_z")

    show_and_reset_smallest_and_highest_memory_usage("vector z step", start_time)

    self.__insert_domain_ranks(clusters, z)
    self.__multiply_phi_value_with_cluster_ranking(cluster_separated_phi, z)

    return self.__cluster_separated_phi_helper.flatten_cluster_separated_phi(cluster_separated_phi)
  
  def __multiply_phi_value_with_cluster_ranking(self, cluster_separated_phi: list[NDArray[float_]], z: NDArray[float_]):
    for cluster_no, phi_per_cluster in enumerate(cluster_separated_phi):
      for local_index in range(phi_per_cluster.shape[0]):
        phi_per_cluster[local_index] *= z[cluster_no]

  def __insert_domain_ranks(self, clusters: dict[str, list[PageInformation]], z: NDArray[float_]):
    domain_ranks: list[float] = []
    cluster_urls = list(clusters.keys())

    for i in range(len(cluster_urls)):
      domain_ranks.append(float(z[i]))

    self.__domain_repository.update_mdpcv2_rank(cluster_urls, domain_ranks)
