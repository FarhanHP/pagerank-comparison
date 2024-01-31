from cache import PCache
from model import PageInformation, PageLinking
from typing import Callable, Optional
from numpy.typing import NDArray
from numpy import float_
from concurrent.futures import ThreadPoolExecutor
from shared_helpers import create_url_to_page_information_dict, full_matrix
from abstracts import Multithreadable
import threading

class PWithCacheHelper(Multithreadable):
  def create_and_dump_p(
    self,
    p_cache: PCache,
    d: float, 
    page_informations: list[PageInformation], 
    get_page_linkings: Callable[[int, Optional[bool]], list[PageLinking]]
  ):
    """
    create matrix P and dump it into cache by modifying p_cache

    Args:
      - p_cache: object to write P matrix into cache
      - d: damping_factor, usually 0.85
      - page_informations: N-length list containing all page informations in database
      - get_page_linkings: function or method to get page linkings of page information id
    """

    print(f"Create and dump P matrix start")

    pages_count = len(page_informations) # N in paper
    url_to_page_information = create_url_to_page_information_dict(page_informations)

    if(self._is_multithread):
      with ThreadPoolExecutor(self._max_workers) as executor:
        executor.map(
          self.__create_and_dump_p_column_values, 
          [pages_count for _ in range(pages_count)], 
          [page_information for page_information in page_informations], 
          [url_to_page_information for _ in range(pages_count)],
          [p_cache for _ in range(pages_count)],
          [get_page_linkings for _ in range(pages_count)],
          [d for _ in range(pages_count)],
        )
    else:
      for i in range(pages_count):
        self.__create_and_dump_p_column_values(
          pages_count, page_informations[i], 
          url_to_page_information, p_cache, 
          get_page_linkings, d)

    print(f"Create and dump P matrix done")
  
  def __create_and_dump_p_column_values(
    self,
    pages_count: int,
    page_information: PageInformation, 
    url_to_page_information: dict[str, PageInformation],
    p_cache: PCache,
    get_page_linkings: Callable[[int, Optional[bool]], list[PageLinking]],
    d: float
  ):
    try:
      p_column = self.__create_p_column_values(pages_count, page_information, url_to_page_information, get_page_linkings, d)
      p_cache.dump_column(page_information.index, p_column)
      print(f"create_and_dump_p_column_values for page_index: {page_information.index} done; thread_id={threading.get_native_id()}")
    except Exception as e:
      print(f"create_and_dump_p_column_values: {e}")

  def __create_p_column_values(
    self,
    pages_count: int,
    page_information: PageInformation, 
    url_to_page_information: dict[str, PageInformation],
    get_page_linkings: Callable[[int, Optional[bool]], list[PageLinking]],
    d: float
  ) -> NDArray[float_]:

    try: # need to wrap it with try block because, in Threadpool, error will not be displayed
      page_linkings = get_page_linkings(page_information.id_page, False) 
      cj = len(page_linkings)
      output = full_matrix(pages_count, (1-d)/pages_count if(cj > 0) else 1/pages_count)

      for page_linking in page_linkings:
        target_page_information: PageInformation

        try:
          target_page_information = url_to_page_information[page_linking.outgoing_link]
        except KeyError as e:
          print(page_linking.outgoing_link)

          raise e

        target_index = target_page_information.index
        output[target_index] = d/cj + (1-d)/pages_count

      return output

    except Exception as e:
      print(f"create_p_column_values: {e}")
      raise e
