import sys, os

sys.path.append(os.path.abspath(os.path.join('')))

from factories import close_db, create_page_rank_random_walkers_repository, create_page_rank_repository, get_db
from scripts.helper import render_number, round_5_decimal_places

def main():
  page_rank_table_names = ["page_rank_original_pagerank_dpc_paper_version", "page_rank_dpc", "page_rank_modified_dpc_v2"]
  page_rank_tables: list[list[tuple[int, float]]] = []
  page_rank_random_walker_rows = create_page_rank_random_walkers_repository().get_page_ids_and_walkers_sorted_by_rank()
  page_rank_random_walker_normalized_rows = get_page_rank_random_walker_normalized_rows(page_rank_random_walker_rows)

  for page_rank_table_name in page_rank_table_names:
    page_rank_tables.append(get_page_ranks(page_rank_table_name))

  length = len(page_rank_tables[0])

  generate_page_rank_comparison_table(page_rank_tables[0], page_rank_tables[1], page_rank_tables[2], page_rank_random_walker_normalized_rows, 0, 50)
  generate_page_rank_comparison_table(page_rank_tables[0], page_rank_tables[1], page_rank_tables[2], page_rank_random_walker_normalized_rows, length-50, length)

  close_db()

def get_page_ranks(table_name: str) -> list[tuple[int, float]]:
  page_rank_repository = create_page_rank_repository(table_name)
  return page_rank_repository.get_page_ids_and_rank_value()

def get_page_rank_random_walker_normalized_rows(page_rank_random_walker_rows: list[tuple[int, int]]) -> list[tuple[int, float]]:
  page_rank_random_walker_normalized_rows: list[tuple[int, float]] = []
  total_walkers_count = sum([row[1] for row in page_rank_random_walker_rows])

  for page_rank_random_walker_row in page_rank_random_walker_rows:
    normalized_value = page_rank_random_walker_row[1]/total_walkers_count
    page_rank_random_walker_normalized_rows.append((page_rank_random_walker_row[0], normalized_value))

  return page_rank_random_walker_normalized_rows

def generate_local_page_rank_comparison_table(
  local_page_rank_modified_dpc_v2_rows: list[tuple[int, float]],
  local_page_rank_dpc_rows: list[tuple[int, float]],
  start: int,
  end: int
):
  for i in range(start, end, 1):
    local_page_rank_modified_dpc_v2_row = local_page_rank_modified_dpc_v2_rows[i]
    local_page_rank_dpc_row = local_page_rank_dpc_rows[i]
    print(f"{i+1} & {local_page_rank_dpc_row[0]} & {round_5_decimal_places(local_page_rank_dpc_row[1])} & {local_page_rank_modified_dpc_v2_row[0]} & {round_5_decimal_places(local_page_rank_modified_dpc_v2_row[1])} \\\\")

def generate_page_rank_comparison_table(
  page_rank_pagerank_rows: list[tuple[int, float]],
  page_rank_dpc_rows: list[tuple[int, float]],
  page_rank_modified_dpc_v2_rows: list[tuple[int, float]],
  page_rank_random_walker_normalized_rows: list[tuple[int, float]] | None,
  start: int,
  end: int 
):
  for i in range(start, end, 1):
    page_rank_pagerank_row = page_rank_pagerank_rows[i]
    page_rank_dpc_row = page_rank_dpc_rows[i]
    page_rank_modified_dpc_v2_row = page_rank_modified_dpc_v2_rows[i]

    page_rank_random_walker_normalized_row: tuple[int, float] | None = None

    if(page_rank_random_walker_normalized_rows != None):
      page_rank_random_walker_normalized_row = page_rank_random_walker_normalized_rows[i]

    print(f"{render_number(i+1)} & {render_page_id_and_rank_value(page_rank_pagerank_row)} & {render_page_id_and_rank_value(page_rank_dpc_row)} & {render_page_id_and_rank_value(page_rank_modified_dpc_v2_row)} & {render_page_id_and_rank_value(page_rank_random_walker_normalized_row)} \\\\")

def render_page_id_and_rank_value(pair: tuple[int, float] | None) -> str:
  if(pair is None):
    return " - & - "
  
  return f"{render_number(pair[0])} & {round_5_decimal_places(pair[1])}"

if (__name__ == "__main__"):
  main()