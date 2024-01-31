def round_5_decimal_places(a: float) -> str:
  return replace_e05_number(str(round(a, 5)).replace(".", ","))

def get_normalized_page_rank_random_walker_score_with_page_ids(page_id_with_random_walker_counts: list[tuple[int, int]]) -> list[tuple[int, float]]:
  walkers_count_total = sum(page_id_with_random_walker_count[1] for page_id_with_random_walker_count in page_id_with_random_walker_counts)
  
  return [(page_id_with_random_walker_count[0], page_id_with_random_walker_count[1]/walkers_count_total) for page_id_with_random_walker_count in page_id_with_random_walker_counts]

# number ex: 10000.342 -> 10.000,342
def render_number(number) -> str:
  number = str(number).split(".")
  rendered_number = ""

  if(len(number) > 1):
    rendered_number = f",{number[1]}"
  
  number = number[0]

  while(len(number) > 3) :
    if(len(rendered_number) > 0):
      rendered_number = f"{number[-3:]}.{rendered_number}"
    else:
      rendered_number = number[-3:]
    number = number[:-3]

  if(len(rendered_number) > 0):
    rendered_number = f"{number}.{rendered_number}"
  else:
    rendered_number = number

  return rendered_number

def replace_e05_number(number: str) -> str:
  if("e-05" not in number):
    return number
  
  return f"0,0000{number.replace('e-05', '')}"