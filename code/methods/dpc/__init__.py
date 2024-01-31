from cache import PCache, QListCache, RPCache, PiiListCache, PastiListCache, PiastListCache
from data.domain_repository import DomainRepository
from model import PageInformation
from shared_helpers import l1_norm, full_matrix, show_and_reset_smallest_and_highest_memory_usage
from numpy.typing import NDArray
from numpy import float_, copy
from methods.dpc.rp_helper import RPHelper
from methods.dpc.partitioned_p_helper import PartitionedPHelper
from methods.dpc.cluster_separated_phi_helper import ClusterSeparatedPhiHelper
from methods.dpc.pasti_helper import PastiHelper
from methods.dpc.piast_helper import PiastHelper
from methods.dpc.extended_local_transition_matrix_helper import ExtendedLocalTransitionMatrixHelper
from typing import cast
from shared_helpers.cluster_helper import ClusterHelper

class DPCExecutor:
  """
  main class for DPC algorithm program
  """

  __p_cache: PCache
  __q_list_cache: QListCache
  __rp_cache: RPCache
  __pii_list_cache: PiiListCache
  __pasti_list_cache: PastiListCache
  __piast_list_cache: PiastListCache

  __rp_helper: RPHelper
  __partitioned_p_helper: PartitionedPHelper
  __cluster_separated_phi_helper: ClusterSeparatedPhiHelper
  __pasti_helper: PastiHelper
  __piast_helper: PiastHelper
  __extended_local_transition_matrix_helper: ExtendedLocalTransitionMatrixHelper
  __cluster_helper: ClusterHelper

  __domain_repository: DomainRepository

  def insert_caches(
    self,
    p_cache: PCache,
    q_list_cache: QListCache,
    rp_cache: RPCache,
    pii_list_cache: PiiListCache,
    pasti_list_cache: PastiListCache,
    piast_list_cache: PiastListCache
  ):
    """
    insert cache classes that will be used later
    """

    self.__p_cache = p_cache
    self.__q_list_cache = q_list_cache
    self.__rp_cache = rp_cache
    self.__pii_list_cache = pii_list_cache
    self.__pasti_list_cache = pasti_list_cache
    self.__piast_list_cache = piast_list_cache

  def insert_helpers(
    self,
    rp_helper: RPHelper,
    partitioned_p_helper: PartitionedPHelper,
    cluster_separated_phi_helper: ClusterSeparatedPhiHelper,
    pasti_helper: PastiHelper,
    piast_helper: PiastHelper,
    extended_local_transition_matrix_helper: ExtendedLocalTransitionMatrixHelper,
    cluster_helper: ClusterHelper,
  ):
    """
    insert helper classes that will be used later
    """

    self.__rp_helper = rp_helper
    self.__partitioned_p_helper = partitioned_p_helper
    self.__cluster_separated_phi_helper = cluster_separated_phi_helper
    self.__pasti_helper = pasti_helper
    self.__piast_helper = piast_helper
    self.__extended_local_transition_matrix_helper = extended_local_transition_matrix_helper
    self.__cluster_helper = cluster_helper


  def insert_repositories(self, domain_repository: DomainRepository):
    """
    insert repository classes that will be used later
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
    entry point for DPC algorithm

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

    page_information_in_clusters = list(clusters.values())
    r = self.__cluster_helper.construct_r(page_information_in_clusters)
    pages_count = self.__cluster_helper.get_all_page_counts(page_information_in_clusters)

    self.__partitioned_p_helper.dump_partitioned_p(
      page_information_in_clusters, 
      self.__p_cache, 
      self.__q_list_cache, 
      self.__pii_list_cache
    )

    show_and_reset_smallest_and_highest_memory_usage("dump_partitioned_p step", start_time)

    cluster_separated_phi = self.__cluster_separated_phi_helper.construct_cluster_separated_phi(
      page_information_in_clusters, 
      self.__q_list_cache, 
      pagerank_dpc, epsilon,
      pagerank_dpc_max_iteration
    )

    show_and_reset_smallest_and_highest_memory_usage("construct_cluster_separated_phi step", start_time)

    self.__rp_helper.dump_and_mult_rp(
      self.__rp_cache, r, 
      self.__p_cache, pages_count
    )

    show_and_reset_smallest_and_highest_memory_usage("dump_and_mult_rp step", start_time)

    self.__pasti_helper.construct_and_dump_pasti_list(
      self.__pasti_list_cache, self.__p_cache, 
      page_information_in_clusters, pages_count
    )

    show_and_reset_smallest_and_highest_memory_usage("construct_and_dump_pasti_list step", start_time)

    self.__piast_helper.construct_and_dump_piast_list(
      self.__piast_list_cache, 
      self.__p_cache, page_information_in_clusters, 
      pages_count
    )

    show_and_reset_smallest_and_highest_memory_usage("construct_and_dump_piast_list step", start_time)

    phi = self.__cluster_separated_phi_helper.flatten_cluster_separated_phi(cluster_separated_phi)
    old_phi = copy(phi)

    print("start iterating...")
    iteration_count = 0
    while True:
      iteration_count += 1
      s = self.__cluster_separated_phi_helper.construct_s(cluster_separated_phi)
      a = self.__rp_cache.load_rp() @ s # A = RPS(phi^k)
      z = pagerank_dpc(full_matrix(a.shape[0], 1/len(clusters)), a, epsilon, pagerank_dpc_max_iteration, f"pagerank_z-{iteration_count}")

      b_list = self.__extended_local_transition_matrix_helper.construct_extended_local_transition_matrice(
        self.__pii_list_cache, 
        self.__piast_list_cache, 
        self.__pasti_list_cache, 
        s, z, cluster_separated_phi, 
        pages_count
      )

      extended_local_pagerank_list = self.__construct_extended_local_pagerank_list(b_list, epsilon, iteration_count, pagerank_dpc_max_iteration)
      cluster_separated_phi = self.__cluster_separated_phi_helper.get_new_cluster_separated_phi(z, extended_local_pagerank_list)
      phi = self.__cluster_separated_phi_helper.flatten_cluster_separated_phi(cluster_separated_phi)
      phi = cast(NDArray[float_], phi/l1_norm(phi))

      delta = l1_norm(phi - old_phi)
      print(f"delta = {delta}")
      if(delta < epsilon or iteration_count >= pagerank_dpc_max_iteration):
        self.__update_domain_ranks(z, clusters)
        break

      old_phi = copy(phi)

    return phi
  
  def __update_domain_ranks(self, z: NDArray[float_], clusters: dict[str, list[PageInformation]]):
    self.__domain_repository.update_dpc_rank(list(clusters.keys()), [float(domain_rank) for domain_rank in z])
  
  def __construct_extended_local_pagerank_list(
    self, b_list: list[NDArray[float_]], epsilon: float, no: int, pagerank_dpc_max_iteration: int
  ) -> list[NDArray[float_]]:
    clusters_count = len(b_list)

    return [pagerank_dpc(
      self.__create_initial_phi(b_list[cluster_no].shape[0]),
      b_list[cluster_no], epsilon, pagerank_dpc_max_iteration,
      f"construct_extended_local_pagerank_list-{no}"
    ) for cluster_no in range(clusters_count)]

  def __create_initial_phi(self, ni_plus_1) -> NDArray[float_]:
    return full_matrix(ni_plus_1, 1/ni_plus_1)
  

def pagerank_dpc(
  phi: NDArray[float_], 
  p: NDArray[float_],
  epsilon: float,
  max_iteration: int,
  log_name: str
) -> NDArray[float_]:
  """
  pagerank computation for DPC algorithm

  Args:
    epsilon: maximum l1 norm difference/delta between pagerank vector current iteration
    p: transition N x N matrix
    phi: initial pagerank N x 1 vector
    max_iteration: iteration maximum 
    log_name: for logging purpose name that will displayed in log for each iteration

  Returns:
    phi: final pagerank N x 1 vector
  """

  new_phi = full_matrix(phi.shape, 0)

  iteration_count = 0
  while True:
    iteration_count += 1
    new_phi: NDArray[float_] = p @ phi
    new_phi = cast(NDArray[float_], new_phi / l1_norm(new_phi))

    if(l1_norm(new_phi - phi) < epsilon or iteration_count >= max_iteration):
      print(f"{log_name} {iteration_count} iteration count")
      return new_phi

    phi = new_phi
