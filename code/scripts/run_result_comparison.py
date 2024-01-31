import os
import sys


sys.path.append(os.path.abspath(os.path.join('')))

from cache import QListCache
from factories import get_db, create_page_information_repository
from shared_helpers import l1_norm, PageInformationsClusterizer
from data.db import DB
from typing import cast
from concurrent.futures import ThreadPoolExecutor
import threading

if(__name__ == "__main__"):

  # print(l1_norm(dpc), dpc.shape)
  # print(l1_norm(original_pagerank), original_pagerank.shape)
  # print(l1_norm(original_pagerank_dpc_paper_version), original_pagerank_dpc_paper_version.shape)
  # print(l1_norm(dpc - original_pagerank))
  # print(l1_norm(dpc - original_pagerank_dpc_paper_version))
  # print(l1_norm(original_pagerank - original_pagerank_dpc_paper_version))

  # count = 0
  # for i in (original_pagerank_dpc_paper_version - original_pagerank):
  #   if(abs(i) > EPSILON):
  #     count += 1

  # print(count)

  page_informations_repository = create_page_information_repository()
  page_informations = page_informations_repository.get_all_page_informations()
  print(len(page_informations))

  clusterizer = PageInformationsClusterizer()
  clusters = clusterizer.clusterize(page_informations)
  clusters_list = [[domain, len(clusters[domain])] for domain in clusters.keys()]
  sorted_clusters_list = sorted(clusters_list, key=lambda cluster: cluster[1], reverse=True)

  for no, cluster in enumerate(sorted_clusters_list):
    print(f"{no+1} & {cluster[0]} & {cluster[1]} \\\\")
    
  
