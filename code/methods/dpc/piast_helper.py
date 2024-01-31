from cache import PiastListCache, PCache
from model import PageInformation
from shared_helpers import full_matrix

class PiastHelper:
  def construct_and_dump_piast_list(self, piast_list_cache: PiastListCache, p_cache: PCache, clusters: list[list[PageInformation]], pages_count: int):
    """
    construct Ni x N Pi* matrix and dump it into cache using piast_list_cache

    Args:
      - piast_list_cache: object to write Pi* matrix into cache
      - p_cache: object to load matrix P from cache
      - clusters: page informations that are grouped by their domain forming n x Ni nested list. First level contain list of page informations that have common domain, while second level contain the page information itself
      - pages_count: all page informations count in the database / N
    """

    print("construct_and_dump_piast_list start")

    for cluster_no in range(len(clusters)):
      self.__construct_and_dump_piast(piast_list_cache, p_cache, clusters[cluster_no], cluster_no, pages_count)

    print("construct_and_dump_piast_list end")

  def __construct_and_dump_piast(self, piast_list_cache: PiastListCache, p_cache: PCache, cluster: list[PageInformation], cluster_no: int, pages_count: int):
    try:
      piast = full_matrix((len(cluster), pages_count), 0)
      min_index = cluster[0].index
      max_index = cluster[-1].index + 1

      for i in range(pages_count):
        piast[:, i] = p_cache.load_column(i)[min_index:max_index]
      
      piast_list_cache.dump_piast(cluster_no, piast)
      print(f"construct_and_dump_piast done for cluster_no = {cluster_no}")

    except Exception as e:
      print(f"construct_and_dump_piast {e}")