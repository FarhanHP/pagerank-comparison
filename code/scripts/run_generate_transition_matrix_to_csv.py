import sys, os

sys.path.append(os.path.abspath(os.path.join('')))

from factories import create_p_helper, create_page_information_repository, create_page_linking_repository, create_x_factory, close_db
from shared_helpers import PageInformationsClusterizer, sort_page_information_by_domain
from consts import DB_NAME, DAMPING_FACTOR, PROJECT_ROOT_PATH

if(__name__ == "__main__"):
  page_information_repository = create_page_information_repository()
  page_informations = page_information_repository.get_all_page_informations()
  clusterizer = PageInformationsClusterizer()
  page_informations = sort_page_information_by_domain(clusterizer.clusterize(page_informations))
  page_linking_repository = create_page_linking_repository()

  p_helper = create_p_helper()
  p = p_helper.create_p(
    DAMPING_FACTOR, 
    page_informations, 
    page_linking_repository.get_page_linkings_by_page_id
  )

  x_factory = create_x_factory()
  x = x_factory.create(page_informations, page_linking_repository.get_page_linkings_by_page_id)

  header0 = ",,"
  header1 = ",,"
  p_bodies: list[str] = []
  x_bodies: list[str] = []
  pages_count = len(page_informations)
  biggest_no_connection_value = (1 - DAMPING_FACTOR)/pages_count # (1-d)/N
  for page_information in page_informations:
    header0 += f"{str(page_information.id_page)},"
    header1 += f"{str(page_information.url)},"

    p_body = f"{page_information.id_page},{page_information.url},{str(list(p[page_information.index])).replace('[', '').replace(']', '').replace(' ', '')}\n"
    x_body = f"{page_information.id_page},{page_information.url},{str(list(x[page_information.index])).replace('[', '').replace(']', '').replace(' ', '')}\n"

    p_bodies.append(p_body)
    x_bodies.append(x_body)
  
  header0 = header0[:-1] + "\n"
  header1 = header1[:-1] + "\n"

  p_matrix_csv_str = header0 + header1
  x_matrix_csv_str = header0 + header1
  for i in range(len(p_bodies)):
    x_body = x_bodies[i]
    x_matrix_csv_str += x_body

    p_body = p_bodies[i]
    p_matrix_csv_str += p_body

  file = open(f"{PROJECT_ROOT_PATH}/scripts/files/{DB_NAME}/p_matrix.csv", "w")
  file.write(p_matrix_csv_str)
  file.close()

  file = open(f"{PROJECT_ROOT_PATH}/scripts/files/{DB_NAME}/x_matrix.csv", "w")
  file.write(x_matrix_csv_str)
  file.close()

  close_db()