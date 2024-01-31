import sys, os

sys.path.append(os.path.abspath(os.path.join('')))

from factories import create_domain_repository, create_page_information_repository
from shared_helpers import PageInformationsClusterizer

def main():
  page_information_repository = create_page_information_repository()
  domain_repository = create_domain_repository()

  page_informations = page_information_repository.get_all_page_informations()
  clusterizer = PageInformationsClusterizer()
  domains = clusterizer.clusterize(page_informations)

  domain_urls = list(domains.keys())
  domain_ids: list[int] = []
  page_ids: list[int] = []
  domain_id_for_pages: list[int] = []

  for i in range(len(domain_urls)):
    domain_url = domain_urls[i]
    page_informations_per_domain = domains[domain_url]
    domain_id = i + 1
    domain_ids.append(domain_id)

    for page_information in page_informations_per_domain:
      page_ids.append(page_information.id_page)
      domain_id_for_pages.append(domain_id)
      print(f"{page_information.id_page} {page_information.url}")

  domain_repository.insert_domains(domain_ids, domain_urls)
  page_information_repository.update_domain_id_by_page_ids(page_ids, domain_id_for_pages)

if(__name__ == "__main__"):
  main()