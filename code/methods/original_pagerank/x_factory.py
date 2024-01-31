from model import PageInformation, PageLinking
from typing import Callable, Optional
from numpy import float_
from numpy.typing import NDArray
from concurrent.futures import ThreadPoolExecutor
from shared_helpers import create_url_to_page_information_dict, full_matrix
from abstracts import Multithreadable
import threading

class XFactory(Multithreadable):
  """
  class that construct X matrix for original pagerank in Sergey Brin and Larry Page paper
  """

  def create(
    self,
    page_informations: list[PageInformation], 
    get_page_linkings_by_page_id: Callable[[int, Optional[bool]], list[PageLinking]]
  ) -> NDArray[float_]:
    """
    create X matrix base on list of PageInformations and get their linkings using get_page_linkings_by_page_id from PageLinkingRepository

    Args:
      page_informations: N-length list containing all PageInformation-s
      get_page_lingkings_by_page_id: method or function to get all page linkings by page information id

    Return:
      N x N "X" matrix, or transition matrix in original pagerank in Larry Page & Sergey Brin paper
    """

    url_to_page_information = create_url_to_page_information_dict(page_informations)

    page_count = len(page_informations)
    x = full_matrix((page_count, page_count), 0)

    if(self._is_multithread):
      with ThreadPoolExecutor(self._max_workers) as executor:
        executor.map(
          self.__fill_X_column_values,
          [x for _ in range(page_count)],
          [page_information for page_information in page_informations],
          [get_page_linkings_by_page_id for _ in range(page_count)],
          [url_to_page_information for _ in range(page_count)]
        )
    else:
      for i in range(page_count):
        self.__fill_X_column_values(x, page_informations[i], get_page_linkings_by_page_id, url_to_page_information)

    return x
  
  def __fill_X_column_values(
    self,
    x: NDArray[float_], page_information: PageInformation, 
    get_page_linkings_by_page_id: Callable[[int, Optional[bool]], list[PageLinking]],
    url_to_page_information: dict[str, PageInformation]
  ):
    try: # need to wrap it with try block because, in Threadpool, error will not be displayed
      page_id = page_information.id_page
      page_linkings = get_page_linkings_by_page_id(page_id, False)
      source_page_index = page_information.index

      for link in page_linkings:
        target_page = self.__get_page_information_by_url(url_to_page_information, link.outgoing_link)

        if(target_page != None):
          target_page_index = target_page.index
          x[target_page_index, source_page_index] = 1/len(page_linkings)

      print(f"fill_X_column_values for page index: {page_information.index} done; thread_id={threading.get_native_id()}")

    except Exception as e:
      print(e)

  def __get_page_information_by_url(
    self,
    url_to_page_information: dict[str, PageInformation], 
    url: str
  ) -> Optional[PageInformation]:
    try:
      return url_to_page_information[url]
    except KeyError:
      return None