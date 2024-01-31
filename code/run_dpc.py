from factories import close_db, create_cluster_separated_phi_helper, create_domain_repository, create_page_information_repository, create_page_informations_clusterizer, create_page_linking_repository, create_page_rank_repository
from shared_helpers import show_and_reset_smallest_and_highest_memory_usage, sort_page_information_by_domain
from cache import PCache, QListCache, RPCache, PiiListCache, PastiListCache, PiastListCache
from consts import DPC_P_MATRIX_PATH, DAMPING_FACTOR, DB_MAX_WORKERS, EPSILON, DPC_Q_MATRIX_PATH, DPC_RP_MATRIX_PATH, DPC_PII_MATRIX_PATH, DPC_PAST_I_MATRIX_PATH, DPC_PI_AST_MATRIX_PATH, IS_MULTITHREAD, PAGERANK_DPC_MAX_ITERATION
from time import time
from methods.dpc.p_with_cache_helper import PWithCacheHelper
from methods.dpc import DPCExecutor
from methods.dpc.rp_helper import RPHelper
from methods.dpc.partitioned_p_helper import PartitionedPHelper
from methods.dpc.pasti_helper import PastiHelper
from methods.dpc.piast_helper import PiastHelper
from methods.dpc.extended_local_transition_matrix_helper import ExtendedLocalTransitionMatrixHelper
import tracemalloc

from shared_helpers.cluster_helper import ClusterHelper

def main():
  start_time = time()
  tracemalloc.start()

  show_and_reset_smallest_and_highest_memory_usage("start", start_time)

  page_information_repository = create_page_information_repository()
  page_informations = page_information_repository.get_all_page_informations()
  clusterizer = create_page_informations_clusterizer()
  clusters = clusterizer.clusterize(page_informations)
  page_informations = sort_page_information_by_domain(clusters)

  p_cache = PCache(DPC_P_MATRIX_PATH)
  q_list_cache = QListCache(DPC_Q_MATRIX_PATH)
  rp_cache = RPCache(DPC_RP_MATRIX_PATH)
  pii_list_cache = PiiListCache(DPC_PII_MATRIX_PATH)
  pasti_list_cache = PastiListCache(DPC_PAST_I_MATRIX_PATH)
  piast_list_cache = PiastListCache(DPC_PI_AST_MATRIX_PATH)

  show_and_reset_smallest_and_highest_memory_usage("initialize step", start_time)

  p_helper = PWithCacheHelper(IS_MULTITHREAD, DB_MAX_WORKERS)
  page_linking_repository = create_page_linking_repository()
  p_helper.create_and_dump_p(p_cache, DAMPING_FACTOR, page_informations, page_linking_repository.get_page_linkings_by_page_id)

  show_and_reset_smallest_and_highest_memory_usage("create_and_dump_p step", start_time)

  rp_helper = RPHelper()
  partitioned_p_helper = PartitionedPHelper()
  cluster_separated_phi_helper = create_cluster_separated_phi_helper()
  pasti_helper = PastiHelper()
  piast_helper = PiastHelper()
  extended_local_transition_matrix_helper = ExtendedLocalTransitionMatrixHelper()
  cluster_helper = ClusterHelper()

  domain_repository = create_domain_repository()

  dpc_executor = DPCExecutor()
  dpc_executor.insert_caches(
    p_cache, q_list_cache, rp_cache, pii_list_cache, 
    pasti_list_cache, piast_list_cache
  )
  dpc_executor.insert_helpers(
    rp_helper, partitioned_p_helper, cluster_separated_phi_helper, 
    pasti_helper, piast_helper, extended_local_transition_matrix_helper,
    cluster_helper
  )
  dpc_executor.insert_repositories(domain_repository)

  print("DPC Start")

  phi = dpc_executor.execute(clusters, EPSILON, PAGERANK_DPC_MAX_ITERATION, start_time)

  show_and_reset_smallest_and_highest_memory_usage("dpc execute step", start_time)
  
  page_rank_repository = create_page_rank_repository("page_rank_dpc")
  page_rank_repository.insert_ranks(page_informations, phi)

  show_and_reset_smallest_and_highest_memory_usage("dpc end", start_time)
  tracemalloc.stop()

  close_db()

if(__name__ == "__main__"):
  main()