"""
this package contain helper classes and functions that are used for all page ranking methods
"""

import tracemalloc
from numpy import float_, full, float64
from numpy.typing import NDArray
from model import PageInformation
from urllib.parse import urlparse
from typing import cast
from time import time
from datetime import datetime

def l1_norm(list: NDArray[float_]) -> float_:
  """
  calculate of level 1 normalization of N x 1 list or vector
  """

  total = cast(float_, 0)
  for i in list:
    total += abs(i)

  return total

def create_url_to_page_information_dict(page_informations: list[PageInformation]) -> dict[str, PageInformation]:
  """
  create a python dictionary with PageInformation.url as key, and the PageInformation itself as the content
  """

  url_to_page_information = {}

  for page_information in page_informations:
    url_to_page_information[page_information.url] = page_information
  
  return url_to_page_information

def sort_page_information_by_domain(clusters: dict[str, list[PageInformation]]) -> list[PageInformation]:
  """
  convert clusters dictionary into PageInformation-s list sorted with following logic:
  
  {"abc.com": [page_information0, page_information1], "aaa.com": [page_information2]} -> [page_information0, page_information1, page_information2]
  """

  page_informations = []
  for cluster in clusters.values():
    for index, page_information in enumerate(cluster):
      page_information.index = len(page_informations) + index
    page_informations += cluster

  return page_informations

class PageInformationsClusterizer:
  """
  helper class related to clusterizing PageInformation-s list into a cluster dictionary
  """

  def clusterize(self, page_informations: list[PageInformation]) -> dict[str, list[PageInformation]]:
    """
    convert PageInformation-s list into a cluster dictionary
    """

    clusters: dict[str, list[PageInformation]] = {}

    for page_information in page_informations:
      
      try:
        domain = self.get_domain(page_information)
        if(domain in clusters.keys()):
          clusters[domain].append(page_information)
        else:
          clusters[domain] = [page_information]
      except TypeError as e:
        print(e)

    return clusters
  
  def get_domain(self, page_information: PageInformation) -> str:
    """
    extract domain from PageInformation.url
    """

    parse_result = urlparse(page_information.url)    
    domain = parse_result.hostname

    if(domain is None):
      raise TypeError(f"cannot get hostname from {page_information.url}")

    if(domain[0:4] == "www."):
        domain = domain[4:]

    return domain

def full_matrix(shape, value: float) -> NDArray[float64]:
  """
  wrapper function to create matrix or factor using numpy.full
  """

  return full(shape, value, dtype=float64)

def show_and_reset_smallest_and_highest_memory_usage(step_name: str, start_time: float | None = None):
  """
  display peak and lowest memory usage, and reset the tracemalloc after that
  """

  traced_memory = tracemalloc.get_traced_memory()
  print("\n==========")
  print(f"{step_name};{get_time_string(start_time)}")
  print(f"smallest memory usage: {traced_memory[0]} Bytes")
  print(f"highest memory usage: {traced_memory[1]} Bytes")
  print("==========\n")
  tracemalloc.reset_peak()

def get_time_string(start_time: float | None) -> str:
  if(start_time is None):
    return ""

  return f" seconds since start: {round(time() - start_time, 3)}; time: {get_datetime_string_now()}"

def get_datetime_string_now() -> str:
  """
  get current datetime string with format YYYY/MM/DD HH:mm:ss
  """

  now = datetime.now()
  return f"{now.year}/{now.month}/{now.day} {now.hour}:{now.minute}:{round(now.second)}"