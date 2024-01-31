from cache import RPCache, PCache
from numpy import float_
from numpy.typing import NDArray
from shared_helpers import full_matrix

class RPHelper:
  def dump_and_mult_rp(
    self, rp_cache: RPCache, r: NDArray[float_], 
    p_cache: PCache, pages_count: int
  ):
    """
    multiply matrix R and matrix P and store the product matrix RP into rp_cache

    Args:
      - rp_cache: object to write RP matrix
      - r: Ni x N matrix R
      - p_cache: object to load matrix P from cache
      - pages_count: all page informations count in the database / N
    """

    rp = full_matrix((r.shape[0], pages_count), 0)

    for col_n in range(pages_count) :
      self.__fill_rp_col(rp[:, col_n], p_cache.load_column(col_n), r, col_n)

    rp_cache.dump_rp(rp)

  def __fill_rp_col(
    self, rp_col: NDArray[float_], p_col: NDArray[float_], 
    r: NDArray[float_], rp_col_no: int
  ):
    try:
      for i in range(len(rp_col)):
        rp_col[i] = r[i] @ p_col

      print(f"dump_and_mult_rp.fill_rp_col col-{rp_col_no} done")
      
    except Exception as e:
      print(f"fill_rp_col: {e}")
