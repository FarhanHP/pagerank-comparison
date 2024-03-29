from pathlib import Path

PROJECT_ROOT_PATH = Path(__file__).parents[1].resolve()

DPC_CACHE_PATH = f"{PROJECT_ROOT_PATH}/cache/dpc"
DPC_P_MATRIX_PATH = f"{DPC_CACHE_PATH}/P"
DPC_Q_MATRIX_PATH = f"{DPC_CACHE_PATH}/Q"
DPC_PII_MATRIX_PATH = f"{DPC_CACHE_PATH}/Pii"
DPC_PI_AST_MATRIX_PATH = f"{DPC_CACHE_PATH}/Pi-ast"
DPC_PAST_I_MATRIX_PATH = f"{DPC_CACHE_PATH}/Past-i"
DPC_RP_MATRIX_PATH = f"{DPC_CACHE_PATH}/RP"

MODIFIED_DPC_V2_CACHE_PATH = f"{PROJECT_ROOT_PATH}/cache/modified_dpc_v2"
MODIFIED_DPC_V2_P_MATRIX_PATH = f"{MODIFIED_DPC_V2_CACHE_PATH}/P"
MODIFIED_DPC_V2_Q_MATRIX_PATH = f"{MODIFIED_DPC_V2_CACHE_PATH}/Q"

CACHED_ORIGINAL_PAGERANK_CACHE_PATH = f"{PROJECT_ROOT_PATH}/cache/cached_original_pagerank"

IS_MULTITHREAD = True

DAMPING_FACTOR = 0.85
EPSILON = 10**-5

DB_MAX_WORKERS = 100 # Max worker for thread that create a db connection
MAX_WORKERS = 100
MAX_ITERATION = 2000
RANDOM_WALKER_ITERATIONS = 20
RANDOM_WALKER_INITIAL_WALKERS_COUNT = 20000
PAGERANK_DPC_MAX_ITERATION = 2000

DB_HOST = "localhost"
DB_PORT = "3306"
DB_USERNAME = "farhanhp" # farhan in laptop & farhanhp in desktop
DB_PASSWORD = "farhanhp123" # farhan123 & farhanhp123 in desktop
DB_NAME = "dpc_crawl" # dpc_crawl_small_data_v2 | dpc_crawl
