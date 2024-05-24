import random
from pathlib import Path
from typing import List
from common_utils.utils import Utils

#!/usr/bin/env python
#
# get_sample_corpus.py
# Gabriel de Jesus (mestregabrieldejesus@gmail.com)
# 17-07-2023


class GetSampleCorpus:
    """ Loads and generates ramdom samples for the corpus quality evaluation. """

    def __init__(
        self,
        corpus_file_path: Path,
        corpus_sample_dir_path: Path,
        total_sample: int,
        total_text_pages: int
    ) -> None:
        self.load_corpus = Utils(corpus_file_path)
        self.corpus_sample_dir_path = corpus_sample_dir_path
        self.total_sample = total_sample
        self.total_text_pages = total_text_pages

    def generate_sample(self) -> List[str]:
        corpus = self.load_corpus.load_sample_corpus()
        for i in range(1, self.total_sample+1, 1):
            ramdom_contents = "\n\n".join(
                random.sample(corpus, self.total_text_pages))
            sample_path = f"{self.corpus_sample_dir_path}/sample_{i}.txt"
            try:
                with open(sample_path, 'w', encoding='utf-8') as f_sample:
                    f_sample.write(ramdom_contents)
            except FileNotFoundError:
                print(f"Folder not found at: {self.corpus_sample_dir_path}")
                return []
        print(
            f"A total of {self.total_sample} samples with {self.total_text_pages} text pages for each have been generated successfully.")
