"""
this package contain Cache classes that act as intermediary between the program and pickle library
"""

from pickle import dump, load
from numpy.typing import NDArray
from numpy import float_
from typing import Any

class Cache:
  """
  Properties:
    - folder_path: .pkl file folder that store .pkl files

  Methods:
    - private create_file(self, file_name: str) -> str
        - create .pkl file

    - protected dump(self, file_name: str, obj: Any)
        - dump object into .pkl file

    - protected load(self, file_name: str) -> Any
        - load .pkl file into python object
  """

  __folder_path: str

  def __init__(self, folder_path: str) -> None:
    self.__folder_path = folder_path

  def __create_file(self, file_name: str) -> str:
    file_location = f"{self.__folder_path}/{file_name}"

    try:
      open(file_location, "x").close()
    except FileExistsError:
      pass
    finally:
      return file_location

  def _dump(self, file_name: str, obj: Any):
    file_location = self.__create_file(file_name)
    with open(file_location, "wb") as file_write:
      dump(obj, file_write)

  def _load(self, file_name: str) -> Any:
    file_location = f"{self.__folder_path}/{file_name}"
    
    try:
      with open(file_location, "rb") as file_open:
        return load(file_open)
    except FileNotFoundError:
      return None

class PCache(Cache):
  """
  caching for P matrix
  
  Properties:
    - file_name: .pkl file name format
  """

  __file_name = "col_{}.pkl"

  def dump_column(self, col_index: int, column: NDArray[float_]):
    """
    dump matrix P by its column into .pkl file / cache
    
    Args:
      - col_index: column index of matrix P
      - column: N x 1 vector of matrix P column
    """

    self._dump(self.__file_name.format(str(col_index)), column)


  def load_column(self, col_index: int) -> NDArray[float_]:
    """
    load P matrix column from .pkl file / cache

    Args:
      - col_index: column index of matrix P
    
    Returns:
      - N x 1 P column vector
    """

    return self._load(self.__file_name.format(str(col_index)))

class QListCache(Cache):
  """
  caching for Q matrix

  Properties:
    - file_name: .pkl file name format
  """

  __file_name = "Q_{}.pkl"

  def dump_q(self, cluster_no: int, q: NDArray[float_]):
    """
    dump Ni x Ni matrix Qi into .pkl file / cache

    Args:
      - cluster_no: "i" number in Qi
      - q: Qi matrix
    """

    self._dump(self.__file_name.format(cluster_no), q)

  def load_q(self, cluster_no: int) -> NDArray[float_]:
    """
    load Ni x Ni matrix Qi from .pkl file / cache

    Args:
      - cluster_no: "i" number in Qi

    Returns:
      Ni x Ni Qi matrix
    """

    return self._load(self.__file_name.format(cluster_no))

class PiiListCache(Cache):
  """
  caching for Pii matrix

  Properties:
    - file_name: .pkl file name format
  """

  __file_name = "P_{}{}.pkl"

  def dump_pii(self, cluster_no: int, pii: NDArray[float_]):
    """
    dump Ni x Ni matrix Pii into cache

    Args:
      - cluster_no: "i" number in Pii
      - pii: Pii matrix
    """

    self._dump(self.__file_name.format(cluster_no, cluster_no), pii)

  def load_pii(self, cluster_no: int) -> NDArray[float_]:
    """
    load Ni x Ni matrix Pii from cache

    Args:
      - cluster_no: "i" number in Pii

    Returns:
      Ni x Ni matrix Pii
    """

    return self._load(self.__file_name.format(cluster_no, cluster_no))

class PiastListCache(Cache):
  """
  caching for Pi* (Pi-ast) matrix

  Properties:
    - file_name: .pkl file name format
  """

  __file_name = "P_{}_ast.pkl"

  def dump_piast(self, cluster_no: int, piast: NDArray[float_]):
    """
    dump Ni x N matrix Pi* into cache

    Args:
      - cluster_no: "i" number in Pi*
      - piast: Pi* matrix
    """

    self._dump(self.__file_name.format(cluster_no), piast)

  def load_piast(self, cluster_no: int) -> NDArray[float_]:
    """
    load Ni x N matrix Pi*  from cache

    Args:
      - cluster_no: "i" number in Pi*

    Returns:
      Ni x N matrix Pi* 
    """

    return self._load(self.__file_name.format(cluster_no))

class PastiListCache(Cache):
  """
  caching for P*i (Past-i) matrix

  Properties:
    - file_name: .pkl file name format
  """

  __file_name = "P_ast_{}.pkl"

  def dump_pasti(self, cluster_no: int, pasti: NDArray[float_]):
    """
    dump N x Ni matrix P*i into cache

    Args:
      - cluster_no: "i" number in P*i
      - pasti: P*i matrix
    """

    self._dump(self.__file_name.format(cluster_no), pasti)

  def load_pasti(self, cluster_no: int) -> NDArray[float_]:
    """
    load N x Ni matrix P*i from cache

    Args:
      - cluster_no: "i" number in P*i
    
    Returns:
      N x Ni matrix P*i
    """

    return self._load(self.__file_name.format(cluster_no))
  
class RPCache(Cache):
  """
  caching for RP matrix

  Properties:
    - file_name: .pkl file name
  """

  __file_name = "RP.pkl"

  def dump_rp(self, rp: NDArray[float_]):
    """
    dump RP matrix into cache

    Args:
      - rp: RP matrix
    """

    self._dump(self.__file_name, rp)

  def load_rp(self) -> NDArray[float_]:
    """
    load RP matrix from cache

    Returns:
      RP matrix
    """

    return self._load(self.__file_name)
