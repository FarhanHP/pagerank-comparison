from pickletools import int4
import sys, os

sys.path.append(os.path.abspath(os.path.join('')))

from factories import create_page_rank_random_walkers_repository, create_page_rank_repository
from data.page_rank_repository import PagerankRepository
from scripts.helper import get_normalized_page_rank_random_walker_score_with_page_ids, round_5_decimal_places
import numpy as np
from consts import DB_NAME


def main():
  print(generate_similarity_score_table(["page_rank_original_pagerank_dpc_paper_version", "page_rank_dpc", "page_rank_modified_dpc_v2"]))

def generate_similarity_score_table(page_rank_table_names: list[str]) -> str:
  page_rank_repositories: list[PagerankRepository] = [create_page_rank_repository(table_name) for table_name in page_rank_table_names]
  page_rank_vectors = [[page_rank_value_with_page_id[1] for page_rank_value_with_page_id in  page_rank_repository.get_page_id_and_rank_value_sorted_by_page_id()] for page_rank_repository in page_rank_repositories]

  page_rank_random_walker_repository = create_page_rank_random_walkers_repository()
  page_rank_random_walker_with_page_ids = get_normalized_page_rank_random_walker_score_with_page_ids(page_rank_random_walker_repository.get_page_id_and_walkers_count_sorted_by_page_id())
  page_rank_vector_random_walker = [page_rank_random_walker_with_page_id[1] for page_rank_random_walker_with_page_id in page_rank_random_walker_with_page_ids]
  page_rank_vectors.append(page_rank_vector_random_walker)

  table_str = ""

  for page_rank_vector_0 in page_rank_vectors:
    for page_rank_vector_1 in page_rank_vectors:
      score = get_kendall_distance_score(page_rank_vector_0, page_rank_vector_1)
      print(score)
      table_str += f"{round_5_decimal_places(score)} & "
      
    table_str = table_str[0:-2] + "\\\\\n"

  return table_str
 
def get_kendall_distance_score(page_ranks0: list[float], page_ranks1: list[float]) -> float:
  pages_count = len(page_ranks0)
  kendall_matrix = np.zeros((pages_count, pages_count), dtype=np.int8)

  for i in range(pages_count):
    for j in range(i+1, pages_count):

      if(page_ranks0[i] >= page_ranks0[j] and page_ranks1[i] < page_ranks1[j]):
        kendall_matrix[i, j] = 1

      if(page_ranks0[i] < page_ranks0[j] and page_ranks1[i] >= page_ranks1[j]):
        kendall_matrix[i, j] = 1

  kendall_matrix_sum = sum(sum(kendall_row) for kendall_row in kendall_matrix)

  return kendall_matrix_sum/(pages_count * (pages_count - 1) / 2)

if(__name__ == "__main__"):
  main()