import sys, os

sys.path.append(os.path.abspath(os.path.join('')))
                
from factories import create_domain_repository

if(__name__ == "__main__"):
  domain_repository = create_domain_repository()
  domains = domain_repository.get_all_domains()
  urls = [domain.url for domain in domains]
  mdpcv2_values = [domain.mdpcv2_rank_value for domain in domains]
  dpc_values = [domain.dpc_rank_value for domain in domains]
  walker_counts = [domain.random_walkers_count for domain in domains]
  walker_counts_normalized = []

  for i in range(len(domains)):
    mdpcv2_values[i] /= sum(mdpcv2_values)
    dpc_values[i] /= sum(dpc_values)
    walker_counts_normalized.append(walker_counts[i] /sum(walker_counts))

  domain_repository.update_domain_walkers_normalized(urls, walker_counts_normalized)
  domain_repository.update_dpc_rank(urls, dpc_values)
  domain_repository.update_mdpcv2_rank(urls, mdpcv2_values)


