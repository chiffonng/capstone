import requests
import json
import logging
from pathlib import Path
from common_utils.tetun_lid import TetunLid
from common_utils.utils import Utils, remove_html_tags

#!/usr/bin/env python
#
# get_corpus.py
# Gabriel de Jesus (mestregabrieldejesus@gmail.com)
# 10-05-2023


class GetCorpus:
    """
    This class:
    (1) Retrieves and load each document from Solr.
    (2) Applies the LID model for each document title and collects only those that satisfy the predefined threshold.
    (3) Saves each title with the respective URL to the final corpus file and applies the LID model to its content.
    (3) Saves each line on the content that satisfies the predefined threshold to the final corpus file.
    """

    def __init__(
        self,
        solr_api_url: str,
        solr_start: int,
        solr_rows: int,
        max_consecutive_newlines: int,
        tetun_lang: str,
        lang_proba_threshold: float,
        lid_model_file_path: Path,
        final_corpus_file_path: Path
    ) -> None:
        self.solr_api_url = solr_api_url
        self.solr_start = solr_start,
        self.solr_rows = solr_rows,
        self.max_consecutive_newlines = max_consecutive_newlines,
        self.tetun_lang = tetun_lang
        self.tetun_lid = TetunLid(
            tetun_lang, lang_proba_threshold, lid_model_file_path)
        self.final_corpus = Utils(final_corpus_file_path)
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s: %(message)s"
        )

    def get_total_documents(self) -> int:
        """ Gets total of documents from Solr and return it. """

        params = {"q": "*:*", "rows": self.solr_rows}
        response = requests.get(self.solr_api_url, params=params)
        response_json = response.json()
        total_doc = response_json["response"]["numFound"]

        return total_doc

    def generate_corpus(self) -> None:
        """
        (1) Retrieve and load each document from the Solr. 
        (2) Apply the Tetun LID model to the document title and collect only those with a probability >= threshold.
        (3) Save title, url and its content that has a proba >= threshold to the final corpus file.
        (4) Add a newline to the end of each document.
        """

        logging.info("Getting and loading json data from Solr...")
        params = {
            "q": "*:*",
            "wt": "json",
            "start": self.solr_start,
            "rows": self.solr_rows
        }

        list_of_titles = []
        start = self.solr_start[0]
        while start < self.get_total_documents():
            params["start"] = start
            response = requests.get(self.solr_api_url, params=params)
            data = json.loads(response.text)
            docs = data["response"]["docs"]

            for doc in docs:
                logging.info("Generating titles...")
                if not doc.get("title") is None:
                    get_title = doc.get("title")

                logging.info("Validating titles...")
                valid_title = self.tetun_lid.get_tetun_text(
                    [get_title])  # Apply the Tetun LID model

                if valid_title and not valid_title in list_of_titles:  # Avoid title duplication
                    list_of_titles.append([get_title])

                    logging.info("Generating page content...")
                    get_url = doc.get("url")
                    get_content = doc.get("content")

                    # Exclude the Urls contain '/feed' and '/tag'.
                    if not '/feed' in get_url and not '/tag' in get_url:
                        # Ensure that only Tetun wikipedia data is processed.
                        if "wikipedia" in get_url and not self.tetun_lang in get_url:
                            logging.warning(
                                f"Not Tetun Wikipedia -> {get_url}.")
                            continue
                        # Excluding facebook since its content was not extracted by Nutch.
                        if "facebook" in get_url:
                            logging.warning(f"Facebook page -> {get_url}.")
                            continue

                        if get_content is None:  # Make sure that the content is not empty.
                            logging.warning(f"Empty content -> {get_title}.")
                            continue

                        self.final_corpus.save_corpus(get_title.strip())
                        self.final_corpus.save_corpus(get_url.strip())

                        consecutive_newlines = 0
                        seen_sentences = set()
                        text_lines = get_content.split("\n")
                        tetun_text = self.tetun_lid.get_tetun_text(
                            text_lines)  # Apply the Tetun LID model
                        for index, doc in enumerate(tetun_text):
                            # Remove HTML tags if exist on the given text
                            text_line = remove_html_tags(doc.strip())
                            if text_line not in seen_sentences:
                                if len(text_line) == 0:
                                    consecutive_newlines += 1
                                else:
                                    consecutive_newlines = 0
                                if len(text_line) == 0 and consecutive_newlines == self.max_consecutive_newlines:
                                    continue
                                else:
                                    self.final_corpus.save_corpus(text_line)
                                    # Add a new line at the end of each non-empty document
                                    if index == len(tetun_text) - 1:
                                        self.final_corpus.save_corpus(
                                            is_not_eol=False)
                                    if len(text_line) > 0:
                                        seen_sentences.add(text_line)
                        logging.info(
                            f"The content was sucessfully generated for the title -> {get_title}")
                    else:
                        logging.warning(
                            f"The URL contains 'feed' or 'tag' -> {get_url}")
                else:
                    logging.warning(
                        f"The title is not in Tetun -> {get_title}")

            # Retrieve the next doc from Solr by incrementing 1 to the start value.
            start += 1

        logging.info("The final corpus has been generated sucessfully.")
