import re
from pathlib import Path
from typing import List
from googlesearch import search
from common_utils.utils import Utils, extract_domain

#!/usr/bin/env python
#
# get_seed_url.py
# Gabriel de Jesus (mestregabrieldejesus@gmail.com)
# 05-07-2023


class GetSeedUrl:
    """
    The GetURL class checks each url if:
    (1) The domain is not on the excluded domain list.
    (2) It is a new seed url.
    (3) It is a new domain.

    After satifying the 1 and 2 conditions:
        * If the url's length is lower than 300, add it to the seed url file.
        * If the url contains a new domain, add it to the domain file.
    """

    def __init__(
        self,
        extension_to_exclude: List[str],
        domains_to_exclude: List[str],
        generate_seed_words: callable,
        google_search_num_result: int,
        max_seed_url_length: int,
        nutch_seed_url_file_path: Path,
        domain_file_path: Path,
    ) -> None:
        self.extension_to_exclude = extension_to_exclude
        self.domains_to_exclude = domains_to_exclude
        self.generate_seed_words = generate_seed_words
        self.google_search_num_result = google_search_num_result
        self.max_seed_url_length = max_seed_url_length
        self.nutch_seed_url_file = Utils(nutch_seed_url_file_path)
        self.domain_file = Utils(domain_file_path)

    def is_allowed_seed_url(self, seed_url: str) -> bool:
        """
        Checks if the given urls' domain is not part of the domain excluded list 
        and it is still not existed on the seed url file.

        :param seed: a seed url.
        :return: True if the url is allowed, False otherwise.
        """

        is_allowed = not any(
            re.search(ext, seed_url.lower()) for ext in self.extension_to_exclude
        ) and not any(domain in seed_url for domain in self.domains_to_exclude)

        return is_allowed

    def is_new_seed_url(self, seed_url: str) -> bool:
        """
        Checks if the given url is new.

        :param seed_url: a seed url.
        :return: True if the url is new, False otherwise.
        """

        new_seed_url = seed_url not in self.nutch_seed_url_file.load_corpus()

        return new_seed_url

    def is_new_domain(self, seed_url: str) -> bool:
        """
        Checks if the input URL's domain contains any of the domains in the domain list.

        :param url: The URL to be checked.
        :return: True if the URL's domain contains any of the domains, False otherwise.
        """

        domain = extract_domain(seed_url)
        new_domain = domain not in self.domain_file.load_corpus()

        return new_domain

    def get_seed_urls(self) -> List[str]:
        """
        Gets new seeds having length < 300 and save them into the seed file 
        and return a list of seed URLs.
        """

        seeds_urls = set()
        for url in search(self.generate_seed_words, num_results=self.google_search_num_result):
            if self.is_allowed_seed_url(url) and self.is_new_seed_url(url):
                seeds_urls.add(url)
                if len(url) < self.max_seed_url_length:
                    self.nutch_seed_url_file.save_corpus(url)

        return list(seeds_urls)

    def get_domains(self, seed_urls: List[str]) -> List[str]:
        """
        Gets new domains from the seed URLs.

        :param seeds: a list of the seed URLs.
        :return: a list of domains.
        """

        domains = set()
        for seed_url in seed_urls:
            domain = extract_domain(seed_url)
            if self.is_new_domain(seed_url):
                domains.add(domain)
                self.domain_file.save_corpus(domain)

        return list(domains)

    def generate_seed_urls(self) -> None:
        """ Gets seed urls returned by the Google search and their respective domains. """

        seed_urls = self.get_seed_urls()
        domains = self.get_domains(seed_urls)

        print(f"\nNew url(s):\n" + "\n".join(seed_urls))
        print(f"\nNew domain(s):\n" + "\n".join(domains))
