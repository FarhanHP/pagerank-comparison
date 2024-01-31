from abstracts import Multithreadable
from typing import Callable, Optional
from numpy.typing import NDArray
from numpy import float_
from model import PageInformation, PageLinking
from concurrent.futures import ThreadPoolExecutor
from shared_helpers import create_url_to_page_information_dict, full_matrix
import threading


class PHelper(Multithreadable):
  """
  Helper class for creating full P matrix without division or caching base on DPC paper
  """

  def create_p(
    self,
    d: float, 
    page_informations: list[PageInformation], 
    get_page_linkings: Callable[[int, Optional[bool]], list[PageLinking]]
  ) -> NDArray[float_]:
    """
    Create full P matrix base on DPC paper without caching or division

    Args:
      - d: damping factor, usually 0.85
      - page_informations: N-length list of PageInformation-s
      - get_page_linkings: method or function to get all page linkings of page information id
    
    Returns:
      N x N "P" matrix or transition matrix
    """

    print(f"Create P matrix start")

    pages_count = len(page_informations) # N in paper
    url_to_page_information = create_url_to_page_information_dict(page_informations)
    p = full_matrix((pages_count, pages_count), 0)

    if(self._is_multithread):
      with ThreadPoolExecutor(self._max_workers) as executor:
        executor.map(
          self.__fill_p_column_values, 
          [p[:, col_no] for col_no in range(pages_count)],
          [pages_count for _ in range(pages_count)], 
          [page_information for page_information in page_informations], 
          [url_to_page_information for _ in range(pages_count)],
          [get_page_linkings for _ in range(pages_count)],
          [d for _ in range(pages_count)],
        )
    else:
      for i in range(pages_count):
        self.__fill_p_column_values(
          p[:, i],
          pages_count, 
          page_informations[i], 
          url_to_page_information, 
          get_page_linkings, 
          d
        )

    print(f"Create P matrix done")
    return p

  def __fill_p_column_values(
    self,
    p_column: NDArray,
    pages_count: int, 
    page_information: PageInformation, 
    url_to_page_information: dict[str, PageInformation],
    get_page_linkings: Callable[[int, Optional[bool]], list[PageLinking]],
    d: float
  ):
    try: # need to wrap it with try block because, in Threadpool, error will not be displayed
      page_linkings = get_page_linkings(page_information.id_page, False) 
      cj = len(page_linkings)

      self.__init_p_column_values(p_column, pages_count, cj, d)

      for page_linking in page_linkings:
        target_page_information: PageInformation

        try:
          target_page_information = url_to_page_information[page_linking.outgoing_link]
        except KeyError as e:
          print(page_linking.outgoing_link)

          raise e

        target_index = target_page_information.index
        p_column[target_index] = d/cj + (1-d)/pages_count

    except Exception as e:
      print(f"create_p_column_values: {e}")

    print(f"fill_p_column_values for page_index = {page_information.index} done; thread_id={threading.get_native_id()}")
    
  def __init_p_column_values(self, p_column: NDArray, pages_count: int, cj: int, d: float):
    initial_p_column_values = full_matrix(pages_count, (1-d)/pages_count if(cj > 0) else 1/pages_count)
      
    for i in range(pages_count):
      p_column[i] = initial_p_column_values[i]
