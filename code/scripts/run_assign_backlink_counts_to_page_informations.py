import sys, os

sys.path.append(os.path.abspath(os.path.join('')))

from factories import create_page_information_repository, create_page_linking_repository
from shared_helpers import PageInformationsClusterizer
from model import Domain

def create_domain_dict(domains: list[Domain]) -> dict[str, Domain]:
  domain_dict: dict[str, Domain] = {}

  for domain in domains:
    domain_dict[domain.url] = domain

  return domain_dict

def main():
  page_linking_repository = create_page_linking_repository()
  page_informations_repository = create_page_information_repository()

  clusterizer = PageInformationsClusterizer()
  page_informations = page_informations_repository.get_all_page_informations()
  clusters = clusterizer.clusterize(page_informations)

  domain_urls = list(clusters.keys())

  for domain_url in domain_urls:
    page_informations_in_domain = clusters[domain_url]

    for page_information in page_informations_in_domain:
      backlink_count = page_linking_repository.get_back_linking_count_by_outgoing_url(page_information.url)
      page_informations_repository.update_backlink_count_by_page_id(page_information.id_page, backlink_count)
      print(f"{page_information.id_page}. {page_information.url}")

if(__name__ == "__main__"):
  main()