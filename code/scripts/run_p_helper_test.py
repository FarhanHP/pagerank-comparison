import sys, os

sys.path.append(os.path.abspath(os.path.join('')))

from factories import create_p_helper
from numpy import array, float32
from scripts.helper.WebGraph import WebGraph

if(__name__ == "__main__"):
  web_graph = WebGraph()

  p_helper = create_p_helper()
  d = 0.5
  p = p_helper.create_p(d, web_graph.page_informations, web_graph.get_page_linking_by_id)

  expected_p = array([
    [1/8, 3/8, 1/8, 1/8],
    [7/24, 1/8, 1/8, 1/8],
    [7/24, 1/8, 1/8, 5/8],
    [7/24, 3/8, 5/8, 1/8]
  ], dtype=float32)
  
  print(p == expected_p)