import sys, os

sys.path.append(os.path.abspath(os.path.join('')))

from scripts.helper.WebGraph import WebGraph
from shared_helpers import PageInformationsClusterizer, sort_page_information_by_domain
from cache import PCache, PastiListCache, PiastListCache, PiiListCache, QListCache, RPCache
from consts import DB_MAX_WORKERS, DPC_P_MATRIX_PATH, DPC_PAST_I_MATRIX_PATH, DPC_PI_AST_MATRIX_PATH, DPC_PII_MATRIX_PATH, DPC_Q_MATRIX_PATH, DPC_RP_MATRIX_PATH, EPSILON, IS_MULTITHREAD, MAX_WORKERS, PAGERANK_DPC_MAX_ITERATION
from methods.dpc.p_with_cache_helper import PWithCacheHelper
from methods.dpc.rp_helper import RPHelper
from factories import create_cluster_separated_phi_helper
from methods.dpc.partitioned_p_helper import PartitionedPHelper
from methods.dpc.extended_local_transition_matrix_helper import ExtendedLocalTransitionMatrixHelper
from methods.dpc.pasti_helper import PastiHelper
from methods.dpc.piast_helper import PiastHelper
from shared_helpers.cluster_helper import ClusterHelper
from methods.dpc import DPCExecutor

if(__name__ == "__main__"):
  web_graph = WebGraph()
  d = 0.5

  page_informations = web_graph.page_informations
  clusterizer = PageInformationsClusterizer()
  clusters = clusterizer.clusterize(page_informations)
  page_informations = sort_page_information_by_domain(clusters)

  p_cache = PCache(DPC_P_MATRIX_PATH)
  q_list_cache = QListCache(DPC_Q_MATRIX_PATH)
  rp_cache = RPCache(DPC_RP_MATRIX_PATH)
  pii_list_cache = PiiListCache(DPC_PII_MATRIX_PATH)
  pasti_list_cache = PastiListCache(DPC_PAST_I_MATRIX_PATH)
  piast_list_cache = PiastListCache(DPC_PI_AST_MATRIX_PATH)

  p_helper = PWithCacheHelper(IS_MULTITHREAD, DB_MAX_WORKERS)
  p_helper.create_and_dump_p(p_cache, d, page_informations, web_graph.get_page_linking_by_id)

  rp_helper = RPHelper()
  partitioned_p_helper = PartitionedPHelper()
  cluster_separated_phi_helper = create_cluster_separated_phi_helper()
  pasti_helper = PastiHelper()
  piast_helper = PiastHelper()
  extended_local_transition_matrix_helper = ExtendedLocalTransitionMatrixHelper()
  cluster_helper = ClusterHelper()

  dpc_executor = DPCExecutor()
  dpc_executor.insert_caches(
    p_cache, q_list_cache, rp_cache, pii_list_cache, 
    pasti_list_cache, piast_list_cache
  )
  dpc_executor.insert_helpers(
    rp_helper, partitioned_p_helper, cluster_separated_phi_helper, 
    pasti_helper, piast_helper, extended_local_transition_matrix_helper,
    cluster_helper
  )

  print("DPC Start")

  phi = dpc_executor.execute(clusters, EPSILON, PAGERANK_DPC_MAX_ITERATION, 0)
  print(phi)