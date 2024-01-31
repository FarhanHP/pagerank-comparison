import sys, os

sys.path.append(os.path.abspath(os.path.join('')))

from factories import create_page_rank_random_walkers_repository, create_page_rank_repository
from scripts.helper import get_normalized_page_rank_random_walker_score_with_page_ids, render_number, round_5_decimal_places
from consts import DB_NAME

def main():
  original_pagerank_list = create_page_rank_repository("page_rank_original_pagerank_dpc_paper_version").get_page_id_and_rank_value_sorted_by_page_id()
  dpc_pagerank_list = create_page_rank_repository("page_rank_dpc").get_page_id_and_rank_value_sorted_by_page_id()
  mdpcv2_pagerank_list = create_page_rank_repository("page_rank_modified_dpc_v2").get_page_id_and_rank_value_sorted_by_page_id()
  random_walker_pagerank_list = get_normalized_page_rank_random_walker_score_with_page_ids(create_page_rank_random_walkers_repository().get_page_id_and_walkers_count_sorted_by_page_id())
  page_count = len(original_pagerank_list)

  if(DB_NAME == "dpc_crawl_small_data_v2"):
    # print(generate_rank_value_difference_table_part1(original_pagerank_list, dpc_pagerank_list, mdpcv2_pagerank_list))
    print(generate_rank_value_difference_table_part2(original_pagerank_list, dpc_pagerank_list, mdpcv2_pagerank_list, random_walker_pagerank_list))

  if(DB_NAME == "dpc_crawl"):
    # print(generate_rank_value_difference_table_part1(original_pagerank_list[0:50], dpc_pagerank_list[0:50], mdpcv2_pagerank_list[0:50]))
    # print(generate_rank_value_difference_table_part1(original_pagerank_list[page_count-50:page_count], dpc_pagerank_list[page_count-50:page_count], mdpcv2_pagerank_list[page_count-50:page_count]))
    print(generate_rank_value_difference_table_part2(original_pagerank_list[0:50], dpc_pagerank_list[0:50], mdpcv2_pagerank_list[0:50], random_walker_pagerank_list[0:50]))
    print(generate_rank_value_difference_table_part2(original_pagerank_list[page_count-50:page_count], dpc_pagerank_list[page_count-50:page_count], mdpcv2_pagerank_list[page_count-50:page_count], random_walker_pagerank_list[page_count-50:page_count]))

def generate_rank_value_difference_table_part1(
  original_pagerank_list: list[tuple[int, float]], 
  dpc_pagerank_list: list[tuple[int, float]],
  mdpcv2_pagerank_list: list[tuple[int, float]]) -> str:

  pages_count = len(original_pagerank_list)
  table_str = ""

  for i in range(pages_count):
    original_pagerank = original_pagerank_list[i][1]
    dpc = dpc_pagerank_list[i][1]
    mdpcv2 = mdpcv2_pagerank_list[i][1]
    page_id = original_pagerank_list[i][0]

    comparison_pair_list = [(original_pagerank, dpc), (original_pagerank, mdpcv2), (dpc, mdpcv2)]

    table_row_str = generate_rank_value_difference_row(comparison_pair_list)
    table_str += f"{render_number(page_id)} & {table_row_str[0:-2]} \\\\\n"

  return table_str

def generate_rank_value_difference_table_part2(
  original_pagerank_list: list[tuple[int, float]], 
  dpc_pagerank_list: list[tuple[int, float]],
  mdpcv2_pagerank_list: list[tuple[int, float]],
  random_walker_pagerank_list: list[tuple[int, float]]) -> str:

  pages_count = len(original_pagerank_list)
  table_str = ""

  for i in range(pages_count):
    original_pagerank = original_pagerank_list[i][1]
    dpc = dpc_pagerank_list[i][1]
    mdpcv2 = mdpcv2_pagerank_list[i][1]
    page_id = original_pagerank_list[i][0]
    random_walker = random_walker_pagerank_list[i][1]

    comparison_pair_list = [(random_walker, original_pagerank), (random_walker, dpc), (random_walker, mdpcv2)]

    table_row_str = generate_rank_value_difference_row(comparison_pair_list)
    table_str += f"{render_number(page_id)} & {table_row_str[0:-2]} \\\\\n"

  return table_str

def generate_rank_value_difference_row(comparison_pair_list: list[tuple[float, float]]) -> str:
  table_row_str = ""

  for comparison_pair in comparison_pair_list:
      table_row_str += f"{round_5_decimal_places(get_difference_value(comparison_pair))} & "
  
  return table_row_str

def get_difference_value(comparison_pair: tuple[float, float]) -> float:
  return abs(comparison_pair[0] - comparison_pair[1])

if(__name__ == "__main__"):
  main()