from cache import PastiListCache, PCache
from model import PageInformation
from shared_helpers import full_matrix

class PastiHelper:
  def construct_and_dump_pasti_list(self, pasti_list_cache: PastiListCache, p_cache: PCache, clusters: list[list[PageInformation]], pages_count: int):
    """
    construct N x Ni P*i matrix and dump it into cache using pasti_list_cache

    Args:
      - pasti_list_cache: object to write P*i matrix into cache
      - p_cache: object to load matrix P from cache
      - clusters: page informations that are grouped by their domain forming n x Ni nested list. First level contain list of page informations that have common domain, while second level contain the page information itself
      - pages_count: all page informations count in the database / N
    """

    print("construct_and_dump_pasti_list start")

    for cluster_no in range(len(clusters)):
      self.__construct_and_dump_pasti(pasti_list_cache, p_cache, clusters[cluster_no], cluster_no, pages_count)

    print("construct_and_dump_pasti_list end")

  def __construct_and_dump_pasti(self, pasti_list_cache: PastiListCache, p_cache: PCache, cluster: list[PageInformation], cluster_no: int, pages_count: int):
    try:
      pasti = full_matrix((pages_count, len(cluster)), 0)
      for index, page in enumerate(cluster):
        pasti[:, index] = p_cache.load_column(page.index)
      
      pasti_list_cache.dump_pasti(cluster_no, pasti)
      print(f"construct_and_dump_pasti done for cluster_no = {cluster_no}")
    except Exception as e:
      print(f"construct_and_dump_pasti {e}")
