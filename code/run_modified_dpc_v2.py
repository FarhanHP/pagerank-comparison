from time import time
import tracemalloc
from cache import PCache, QListCache
from consts import DB_MAX_WORKERS, DAMPING_FACTOR, EPSILON, IS_MULTITHREAD, MODIFIED_DPC_V2_P_MATRIX_PATH, MODIFIED_DPC_V2_Q_MATRIX_PATH, PAGERANK_DPC_MAX_ITERATION
from factories import close_db, create_cluster_separated_phi_helper, create_domain_repository, create_page_information_repository, create_page_linking_repository, create_page_rank_repository
from methods.dpc.p_with_cache_helper import PWithCacheHelper
from methods.modified_dpc_v2.q_helper import QHelper
from methods.modified_dpc_v2 import ModifiedDPCV2Executor
from methods.modified_dpc_v2.a_helper import AHelper
from shared_helpers import PageInformationsClusterizer, show_and_reset_smallest_and_highest_memory_usage, sort_page_information_by_domain

def main():
  start_time = time()
  tracemalloc.start()

  show_and_reset_smallest_and_highest_memory_usage("start", start_time)

  page_information_repository = create_page_information_repository()
  page_informations = page_information_repository.get_all_page_informations()
  clusterizer = PageInformationsClusterizer()
  clusters = clusterizer.clusterize(page_informations)
  page_informations = sort_page_information_by_domain(clusters)

  p_cache = PCache(MODIFIED_DPC_V2_P_MATRIX_PATH)
  q_list_cache = QListCache(MODIFIED_DPC_V2_Q_MATRIX_PATH)
  show_and_reset_smallest_and_highest_memory_usage("instantiate step", start_time)

  p_helper = PWithCacheHelper(IS_MULTITHREAD, DB_MAX_WORKERS)
  page_linking_repository = create_page_linking_repository()
  p_helper.create_and_dump_p(p_cache, DAMPING_FACTOR, page_informations, page_linking_repository.get_page_linkings_by_page_id)
  show_and_reset_smallest_and_highest_memory_usage("create and dump matrix P step", start_time)

  q_helper = QHelper()
  a_helper = AHelper()
  cluster_separated_phi_helper = create_cluster_separated_phi_helper()

  domain_repository = create_domain_repository()

  print("Modified DPC V2 Start")

  modified_dpc_executor = ModifiedDPCV2Executor()
  modified_dpc_executor.insert_caches(p_cache, q_list_cache)
  modified_dpc_executor.insert_helpers(q_helper, cluster_separated_phi_helper, a_helper)
  modified_dpc_executor.insert_repositories(domain_repository)

  show_and_reset_smallest_and_highest_memory_usage("prepare to execution step", start_time)

  phi = modified_dpc_executor.execute(clusters, EPSILON, PAGERANK_DPC_MAX_ITERATION, start_time)

  show_and_reset_smallest_and_highest_memory_usage("after execution step", start_time)

  page_rank_repository = create_page_rank_repository("page_rank_modified_dpc_v2")
  page_rank_repository.insert_ranks(page_informations, phi)

  show_and_reset_smallest_and_highest_memory_usage("modified dpc v2 end", start_time)
  tracemalloc.stop()

  close_db()

if(__name__ == "__main__"):
  main()