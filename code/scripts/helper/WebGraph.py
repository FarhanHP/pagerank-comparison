from typing import Optional
from model import PageInformation, PageLinking


class WebGraph:
  __page_1: PageInformation
  __page_2: PageInformation
  __page_3: PageInformation
  __page_4: PageInformation
  __page_5: PageInformation
  __page_6: PageInformation
  __page_7: PageInformation

  page_informations: list[PageInformation]

  def __init__(self) -> None:
    self.__page_1 = PageInformation(0, 0, "http://unj.ac.id")
    self.__page_2 = PageInformation(1, 1, "http://unj.ac.id/sejarah-unj")
    self.__page_3 = PageInformation(2, 2, "http://unj.ac.id/visi-misi")
    self.__page_4 = PageInformation(3, 3, "http://youtube.com/watch?v=JJ0pP0kzLxQ")
    self.__page_5 = PageInformation(4, 4, "http://youtube.com/watch?v=lz7i_feJWOM")
    self.__page_6 = PageInformation(5, 5, "http://instagram.com/unj_official")
    self.__page_7 = PageInformation(6, 6, "instagram.com/unj_official/followers")
    self.page_informations = [self.__page_1, self.__page_2, self.__page_3, self.__page_4, self.__page_5, self.__page_6, self.__page_7]

  def get_page_linking_by_id(self, id: int, _: Optional[bool]) -> list[PageLinking]:
    if(id == self.__page_1.id_page):
      return [PageLinking(self.__page_2.url), PageLinking(self.__page_3.url), PageLinking(self.__page_4.url), PageLinking(self.__page_6.url)]
    if(id == self.__page_4.id_page):
      return [PageLinking(self.__page_5.url), PageLinking(self.__page_6.url)]
    if(id == self.__page_6.id_page):
      return [PageLinking(self.__page_7.url)]
    
    return []