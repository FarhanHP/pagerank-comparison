class Multithreadable:
  """
  an abstract class for a class that has multithread implementation

  Properties:
    - is_multithread: if true will use multithread implementation
    - max_workers: maximum workers count for ThreadPollExecutor
  """

  _is_multithread: bool
  _max_workers: int

  def __init__(self, is_multithread: bool, max_workers: int) -> None:
    self._is_multithread = is_multithread
    self._max_workers = max_workers