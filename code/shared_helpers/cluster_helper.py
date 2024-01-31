from model import PageInformation
from numpy.typing import NDArray
from numpy import float_

from shared_helpers import full_matrix


class ClusterHelper:
  """
  helper related to cluster
  """

  def construct_r(self, clusters: list[list[PageInformation]]) -> NDArray[float_]:
    """
    create R matrix in DPC from nested list of PageInformation-s that separated base on their domains
    """

    r = full_matrix((len(clusters), self.get_all_page_counts(clusters)), 0)
    for index, cluster in enumerate(clusters):
      for page_information in cluster:
        r[index, page_information.index] = 1

    return r

  def get_all_page_counts(self, clusters: list[list[PageInformation]]) -> int:
    """
    get page counts from nested list of PageInformation-s that separated base on their domains
    """

    n = 0

    for cluster in clusters:
      n += len(cluster)

    return n