import sys, os
from pickle import dump

sys.path.append(os.path.abspath(os.path.join('')))

from consts import PROJECT_ROOT_PATH
from shared_helpers import full_matrix

def dump_obj(obj):
  with open(f"{PROJECT_ROOT_PATH}/cache/test.pkl", "wb") as file_write:
    dump(obj, file_write)

def dump_a():
  a = full_matrix((20000, 100000), 0)
  dump_obj(a)

# experiment result https://stackoverflow.com/questions/13871152/why-pickle-eat-memory. When pickle dump a data, it will make a copy and then put it into file

if(__name__ == "__main__"):
  dump_a()