from abstracts import Multithreadable
from concurrent.futures import ThreadPoolExecutor
from model import PageInformation
from cache import QListCache
from numpy import float_, concatenate, array
from numpy.typing import NDArray
from typing import Callable
from shared_helpers import full_matrix

class ClusterSeparatedPhiHelper(Multithreadable):
  def construct_cluster_separated_phi(
    self, 
    clusters: list[list[PageInformation]], 
    q_list_cache: QListCache, 
    pagerank_dpc: Callable[[NDArray[float_], NDArray[float_], float, int, str], NDArray[float_]],
    epsilon: float,
    pagerank_dpc_max_iteration: int
  ) -> list[NDArray[float_]]:
    """
    contruct Ni x 1 pagerank vector for each cluster/domain

    Args:
      - clusters: page informations that are grouped by their domain forming n x Ni nested list. First level contain list of page informations that have common domain, while second level contain the page information itself
      - q_list_cache: object to access matrix Q in cache
      - pagerank_dpc: function or method to computing pagerank computation
      - epsilon: maximum l1 norm difference/delta between pagerank vector current iteration
      - pagerank_dpc_max_iteration: max iteration for pagerank computation

    Returns:
      n-length list containing Nix1 pagerank vektor
    """

    return [
      pagerank_dpc(
        full_matrix(len(clusters[cluster_no]),1/len(clusters[cluster_no])),
        q_list_cache.load_q(cluster_no),
        epsilon,
        pagerank_dpc_max_iteration,
        f"cluster_separated_phi-{cluster_no}"
      ) for cluster_no in range(len(clusters))
    ]

  def flatten_cluster_separated_phi(self, clusters_separated_phi: list[NDArray[float_]]) -> NDArray[float_]:
    """
    flatten n-length list of Nix1 pagerank vector that still separated by its cluster into N x 1 pagerank vector

    ex: [[0.1, 0.2], [0.3]] -> [0.1, 0.2, 0.3]

    Args:
      - clusters_separated_phi: n-length list containing Nix1 pagerank vektor
    
    Returns:
      N x 1 pagerank vector
    """

    output = array([])
    for phi in clusters_separated_phi:
      output = concatenate((output, phi), axis = 0)

    return output
  
  def get_new_cluster_separated_phi(
    self, z: NDArray[float_],
    extended_local_pagerank_list: list[NDArray[float_]]
  ) -> list[NDArray[float_]]:
    """
    get new cluster separated phi base on "z" vector and extended local pagerank vectors see DPC algorithm in the paper for detail

    Args:
      - z: n x 1 cluster rank vector
      - extended_local_pagerank_list: n-length list containing (Ni+1) x 1 extended local pagerank/extended cluster-separated phi

    Returns:
      n-length list containing new Ni x 1 local pagerank/extended cluster-separated phi vector
    """

    clusters_count = len(extended_local_pagerank_list)

    return [
      self.__update_phi_per_cluster(
        z[cluster_no], extended_local_pagerank_list[cluster_no]
      ) for cluster_no in range(clusters_count)
    ]
      
  def __update_phi_per_cluster(
    self, z_cluster: float,
    extended_local_pagerank: NDArray[float_]
  ) -> NDArray[float_]:
    beta = extended_local_pagerank[-1]
    omega = extended_local_pagerank[0:-1]

    return (1 - z_cluster)/beta * omega
    
  def construct_s(self, cluster_separated_phi: list[NDArray[float_]]) -> NDArray[float_]:
    """
    construct N x n matrix S

    Args:
      - cluster_separated_phi: n-length list containing Ni x 1 local pagerank vector

    Returns:
      N x n matrix S
    """

    pages_count = self.__get_pages_count(cluster_separated_phi)
    s = full_matrix((pages_count, len(cluster_separated_phi)), 0)
    row_index = 0
    for col_index, phi in enumerate(cluster_separated_phi):
      s[row_index:row_index+len(phi), col_index] = phi
      row_index += len(phi)
    return s
  
  def __get_pages_count(self, cluster_separated_phi: list[NDArray[float_]]) -> int:
    pages_count = 0
    for phi in cluster_separated_phi:
      pages_count += phi.shape[0]

    return pages_count
  