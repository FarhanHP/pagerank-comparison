import subprocess

modules = [
    "abstracts", "cache", "data", "factories", "methods", "model", 
    "shared_helpers", "run_dpc", "run_modified_dpc_v2", 
    "run_original_pagerank_dpc_paper_version", "run_random_walker"]

command = f"pdoc --html {' '.join(modules)} --force"

subprocess.call(command, shell=True)