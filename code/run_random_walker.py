
from time import time
import tracemalloc
from factories import close_db, create_random_walker_executor


def main():
  tracemalloc.start()
  start_time = time()
  
  random_walker_executor = create_random_walker_executor()
  random_walker_executor.execute()

  traced_memory = tracemalloc.get_traced_memory()

  print("random walker")
  print(f"smallest memory usage: {traced_memory[0]} Bytes")
  print(f"highest memory usage: {traced_memory[1]} Bytes")
  print(f"{time() - start_time} seconds")

  tracemalloc.stop()
  close_db()

if(__name__ == "__main__"):
  main()