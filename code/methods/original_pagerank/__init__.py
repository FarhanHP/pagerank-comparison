from numpy.typing import NDArray
from numpy import float_
from shared_helpers import l1_norm

def pagerank(
  phi: NDArray[float_], 
  e: NDArray[float_],
  x: NDArray[float_],
  epsilon: float,
  max_iteration: int,
) -> NDArray[float_]:
  """
  page rank computation from Sergey Brin and Larry Page paper

  Args:
    e: epsilon, maximum l1 norm difference/delta between pagerank vector current iteration
    x: transition N x N matrix
    phi: initial pagerank N x 1 vector
    max_iteration: iteration maximum 

  Returns:
    phi: final pagerank N x 1 vector
  """

  iteration = 0

  while True:
    new_phi = x @ phi
    delta = l1_norm(phi) - l1_norm(new_phi)
    new_phi = new_phi + delta * e

    delta = l1_norm(new_phi - phi)
    print(f"iteration: {iteration}; delta: {delta}")

    if(delta < epsilon or iteration > max_iteration):
      return new_phi

    phi = new_phi
    iteration += 1