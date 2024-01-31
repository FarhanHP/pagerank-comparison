from cache import PiiListCache, PiastListCache, PastiListCache
from numpy.typing import NDArray
from numpy import float_
from shared_helpers import full_matrix

class ExtendedLocalTransitionMatrixHelper:
  def construct_extended_local_transition_matrice(
    self, pii_list_cache: PiiListCache, piast_list_cache: PiastListCache, 
    pasti_list_cache: PastiListCache, s: NDArray[float_], z: NDArray[float_],
    cluster_separated_phi: list[NDArray[float_]], pages_count: int
  ) -> list[NDArray[float_]]:
    """
    construct n-length list containing (Ni+1) x (Ni+1) extended local transition matrix, refer to the DPC paper for more detail

    Args:
      - pii_list_cache: object to access Ni x Ni "pii" matrix in cache
      - piast_list_cache: object to access Ni x N "pi*" matrix in cache
      - pasti_list_cache: object to access N x Ni "p*i" matrix in cache
      - s: N x n "s" matrix
      - z: n x 1 cluster rank vector
      - cluster_separated_phi: n-length list containing Ni x 1 local pagerank
      - pages_count: all page informations count in database or known as N

    Returns:
      n-length list containing (Ni+1) x (Ni+1) extended local transition matrix
    """

    clusters_count = len(cluster_separated_phi)

    return [self.__construct_extended_local_transition_matrix(
      pii_list_cache,
      piast_list_cache,
      pasti_list_cache,
      s, z, cluster_separated_phi[cluster_no], 
      cluster_no, pages_count
    ) for cluster_no in range(clusters_count)]
    
  def __construct_extended_local_transition_matrix(
    self, pii_list_cache: PiiListCache, piast_list_cache: PiastListCache, pasti_list_cache: PastiListCache,
    s: NDArray[float_], z: NDArray[float_], cluster_phi: NDArray[float_], cluster_no: int, pages_count: int
  ) -> NDArray[float_]:
    ni = cluster_phi.shape[0]
    b = full_matrix((ni + 1, ni + 1), 0)
    b[0:ni, 0:ni] = pii_list_cache.load_pii(cluster_no)
    b[ni, 0:ni] = full_matrix(pages_count, 1) @ pasti_list_cache.load_pasti(cluster_no)
    right_most_col = full_matrix(ni+1, 0)
    piast_s_z = piast_list_cache.load_piast(cluster_no) @ s @ z
    right_most_col[0:ni] = (piast_s_z - (pii_list_cache.load_pii(cluster_no) @ cluster_phi * z[cluster_no]))/(1-z[cluster_no])
    right_most_col[ni] = 1 - sum(right_most_col)

    return b