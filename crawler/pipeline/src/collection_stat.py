import os
import requests
import numpy as np
import logging
import warnings
from pathlib import Path
from bs4 import BeautifulSoup
from bs4.builder import ParserRejectedMarkup
from requests import exceptions
from common_utils.utils import Utils, extract_domain

warnings.filterwarnings("ignore")

#!/usr/bin/env python
#
# collection_stat.py
# Gabriel de Jesus (mestregabrieldejesus@gmail.com)
# 15-07-2023


class CollectionStatistic:
    """ 
    This class generates the corpus summary comprises:
    (1) Total inlinks and outlinks per document (url).
    (2) Total documents.  
    (3) Total documents per domain.
    (4) Total documents per extension.
    """

    def __init__(
        self,
        final_corpus_file_path: Path,
        url_in_out_links_file_path: Path,
        stats_in_out_links_file_path: Path
    ) -> None:
        self.final_corpus_file_path = Utils(final_corpus_file_path)
        self.url_in_out_links = Utils(url_in_out_links_file_path)
        self.stats_in_out_links_file_path = Utils(stats_in_out_links_file_path)
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s: %(message)s"
        )

    def generate_stats(self) -> None:
        """ Load the final corpus and get the URLs, extract domains and extensions as well as inlinks and outlinks. """

        logging.info("Generating statistics for the collection...")
        corpus = self.final_corpus_file_path.load_final_corpus()
        domain_counts = {}
        extension_counts = {}
        outlink_count_list = []
        inlink_count_list = []
        total_documents = 0
        for conten in corpus.split('\n\n'):
            try:
                url = conten.split('\n')[1].strip()
                total_documents += 1
                # Domains
                domain = extract_domain(url)
                if domain in domain_counts:
                    domain_counts[domain] += 1
                else:
                    domain_counts[domain] = 1

                # Extensions - extract the last part of the URL
                filename = os.path.basename(url)
                extension = os.path.splitext(
                    filename)[1].lower() if '.' in filename else ''
                # Uniformize the Ms. Office extensions
                if extension == 'doc':
                    extension = 'docx'
                elif extension == 'xls':
                    extension = 'xlsx'
                elif extension in ['ppt', 'pps', 'ppsx']:
                    extension = 'pptx'

                if extension in extension_counts:
                    extension_counts[extension] += 1
                else:
                    extension_counts[extension] = 1

                try:
                    # Outlinks and Inlinks for each URL
                    response = requests.get(url)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        links = soup.find_all('a')

                        outlink_count = 0
                        inlink_count = 0
                        for link in links:
                            href = link.get('href')
                            if href and (href.startswith('http://') or href.startswith('https://')):
                                if domain not in href:
                                    outlink_count += 1
                                else:
                                    inlink_count += 1
                            elif href and not href.startswith('#'):
                                inlink_count += 1

                        outlink_count_list.append(outlink_count)
                        inlink_count_list.append(inlink_count)
                        self.url_in_out_links.save_corpus(
                            f"Url: {url}, Outlink: {outlink_count}, Inlink: {inlink_count}")
                    else:
                        continue
                except (exceptions.RequestException, exceptions.ConnectionError, exceptions.HTTPError, exceptions.Timeout,
                        exceptions.TooManyRedirects, exceptions.URLRequired, ParserRejectedMarkup, AssertionError):
                    continue
            except IndexError:
                continue

        # Save the inlinks and outlinks summary
        stat_inlinks_outlinks = f""" Statistics of the collection:
        ========================================
        Total web pages (urls) processed: {total_documents}\n
        Max outlinks: {max(outlink_count_list)}, Min outlinks: {min(outlink_count_list)}, Average oulinks: {np.mean(outlink_count_list):.2f}
        Max inlinks: {max(inlink_count_list)}, Min inlinks: {min(inlink_count_list)}, Average inlinks: {np.mean(inlink_count_list):.2f}
        ========================================
        """
        self.stats_in_out_links_file_path.save_corpus(
            stat_inlinks_outlinks.strip())

        self.stats_in_out_links_file_path.save_corpus(
            f"\n========= Domain: total documents in the corresponding domain =========")
        sorted_domain_items = sorted(
            domain_counts.items(), key=lambda x: x[1], reverse=True)
        for domain, count in sorted_domain_items:
            self.stats_in_out_links_file_path.save_corpus(
                f"Domain: {domain}, total_docs: {count}")

        self.stats_in_out_links_file_path.save_corpus(
            f"\n========= Extension: total documents with the corresponding extension =========")
        sorted_extension_items = sorted(
            extension_counts.items(), key=lambda x: x[1], reverse=True)
        for extension, count in sorted_extension_items:
            self.stats_in_out_links_file_path.save_corpus(
                f"Extension: {extension}, total_docs: {count}")

        logging.info("The statistics have been generated sucessfully.")
