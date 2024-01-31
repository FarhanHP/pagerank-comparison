import sys, os

sys.path.append(os.path.abspath(os.path.join('')))

from factories import create_x_factory
from numpy import array, float32
from scripts.helper.WebGraph import WebGraph

if(__name__ == "__main__"):
  web_graph = WebGraph()

  x_factory = create_x_factory()
  x = x_factory.create(web_graph.page_informations, web_graph.get_page_linking_by_id)

  expected_x = array([
    [0, 1/2, 0, 0],
    [1/3, 0, 0, 0],
    [1/3, 0, 0, 1],
    [1/3, 1/2, 1, 0]
  ], dtype=float32)

  print(x == expected_x)