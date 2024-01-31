import sys, os

sys.path.append(os.path.abspath(os.path.join('')))

from scripts.helper.WebGraph import WebGraph
from shared_helpers import full_matrix
from factories import create_x_factory
from methods.original_pagerank import pagerank

if(__name__ == "__main__"):
  web_graph = WebGraph()
  page_count = len(web_graph.page_informations)
  x_factory = create_x_factory()
  x = x_factory.create(web_graph.page_informations, web_graph.get_page_linking_by_id)
  initial_phi = full_matrix(page_count, 1/page_count)
  e = full_matrix(page_count, 1/page_count)
  phi = pagerank(initial_phi, e, x, 10**-5, 10000)

  print(phi)