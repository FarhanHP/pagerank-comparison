from typing import cast
from numpy.typing import NDArray
from numpy import float_
from shared_helpers import l1_norm

def pagerank_dpc_paper_version(
  phi: NDArray[float_], 
  p: NDArray[float_],
  epsilon: float,
  max_iteration: int
) -> NDArray[float_]:
  """
  page rank computation from DPC paper

  Args:
    epsilon: maximum l1 norm difference/delta between pagerank vector current iteration
    p: transition N x N matrix
    phi: initial pagerank N x 1 vector
    max_iteration: iteration maximum 

  Returns:
    phi: final pagerank N x 1 vector
  """

  iteration = 0

  while True:
    new_phi = cast(NDArray[float_], p @ phi)
    new_phi = cast(NDArray[float_], new_phi / l1_norm(new_phi))

    delta = l1_norm(phi - new_phi)
    print(f"iteration={iteration}; delta={delta}")

    if(delta < epsilon or iteration > max_iteration):
      return new_phi

    iteration += 1
    phi = new_phi
  