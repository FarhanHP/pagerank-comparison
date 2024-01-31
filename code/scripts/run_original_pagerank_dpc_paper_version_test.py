import sys, os

sys.path.append(os.path.abspath(os.path.join('')))

from consts import DAMPING_FACTOR
from numpy import array
from factories import create_p_helper
from methods.original_pagerank_dpc_paper_version.pagerank import pagerank_dpc_paper_version
from shared_helpers import full_matrix

from scripts.helper.WebGraph import WebGraph

if(__name__ == "__main__"):
  # web_graph = WebGraph()
  # page_count = len(web_graph.page_informations)
  # p_helper = create_p_helper()
  # p = p_helper.create_p(DAMPING_FACTOR, web_graph.page_informations, web_graph.get_page_linking_by_id)
  # print(p)
  # initial_phi = full_matrix(page_count, 1/page_count)
  # phi = pagerank_dpc_paper_version(initial_phi, p, 10**-5, 10000000000)

  # print(phi)

  a = array([[0.02143, 0.14286, 0.14286, 0.10025],
       [0.23393, 0.14286, 0.14286, 0.10025],
       [0.23393, 0.14286, 0.14286, 0.10025],
       [1.00001, 1.00002, 1.00002, 0.69924]])
  
  initial_z = array([1/4, 1/4, 1/4, 1/4])
  z = pagerank_dpc_paper_version(initial_z, a, 10**-5, 1000)
  print(z)