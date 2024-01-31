from factories import close_db, create_page_information_repository, create_page_linking_repository, create_page_rank_repository, create_x_factory
from shared_helpers import sort_page_information_by_domain, PageInformationsClusterizer, full_matrix
from consts import EPSILON, MAX_ITERATION
from methods.original_pagerank import pagerank
from time import time

import tracemalloc

if(__name__ == "__main__"):
  tracemalloc.start()
  start_time = time()

  page_information_repository = create_page_information_repository()
  page_informations = page_information_repository.get_all_page_informations()

  clusterizer = PageInformationsClusterizer()
  page_informations = sort_page_information_by_domain(clusterizer.clusterize(page_informations))
  page_linking_repository = create_page_linking_repository()
  x_factory = create_x_factory()
  x = x_factory.create(page_informations, page_linking_repository.get_page_linkings_by_page_id)

  phi = full_matrix(len(x), 1/len(x))
  e = full_matrix(len(x), 1/len(x))
  phi = pagerank(phi, e, x, EPSILON, MAX_ITERATION)

  page_rank_repository = create_page_rank_repository("page_rank_original_pagerank")
  page_rank_repository.insert_ranks(page_informations, phi)

  traced_memory = tracemalloc.get_traced_memory()

  print("original pagerank")
  print(f"smallest memory usage: {traced_memory[0]} Bytes")
  print(f"highest memory usage: {traced_memory[1]} Bytes")
  print(f"{time() - start_time} seconds")

  tracemalloc.stop()
  close_db()