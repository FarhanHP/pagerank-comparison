from factories import close_db, create_p_helper, create_page_information_repository, create_page_informations_clusterizer, create_page_linking_repository, create_page_rank_repository
from methods.original_pagerank_dpc_paper_version.pagerank import pagerank_dpc_paper_version
from consts import DAMPING_FACTOR, MAX_ITERATION, EPSILON
from shared_helpers import show_and_reset_smallest_and_highest_memory_usage, sort_page_information_by_domain, full_matrix
from time import time
import tracemalloc

def main():
  start_time = time()
  tracemalloc.start()
  show_and_reset_smallest_and_highest_memory_usage("start", start_time)
  
  page_information_repository = create_page_information_repository()
  page_informations = page_information_repository.get_all_page_informations()
  clusterizer = create_page_informations_clusterizer()
  page_informations = sort_page_information_by_domain(clusterizer.clusterize(page_informations))
  page_linking_repository = create_page_linking_repository()
  p_helper = create_p_helper()
  show_and_reset_smallest_and_highest_memory_usage("instantiate step", start_time)


  p = p_helper.create_p(
    DAMPING_FACTOR, 
    page_informations, 
    page_linking_repository.get_page_linkings_by_page_id
  )
  show_and_reset_smallest_and_highest_memory_usage("create p matrix step", start_time)

  phi = full_matrix(len(p), 1/len(p))
  phi = pagerank_dpc_paper_version(phi, p, EPSILON, MAX_ITERATION)
  show_and_reset_smallest_and_highest_memory_usage("computation step", start_time)
  
  page_rank_repository = create_page_rank_repository("page_rank_original_pagerank_dpc_paper_version")
  page_rank_repository.insert_ranks(page_informations, phi)

  show_and_reset_smallest_and_highest_memory_usage("original pagerank end", start_time)
  close_db()
  tracemalloc.stop()

if(__name__ == "__main__"):
  main()
