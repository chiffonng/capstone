from dataclasses import dataclass
from typing import List

#!/usr/bin/env python
#
# config.py
# Gabriel de Jesus (mestregabrieldejesus@gmail.com)
# 20-07-2023


""" This module contains soft configuration of the pipeline. """


@dataclass
class Paths:
    data: str
    nutch: str
    lid: str
    eval_sample: str


@dataclass
class Files:
    main_corpus: str
    seed_words: str
    nutch_seed_url: str
    domain: str
    lid_model: str
    final_corpus: str
    stats_in_out_links: str
    url_in_out_links: str


@dataclass
class Params:
    solr_api_url: str
    solr_start: int
    solr_rows: int
    language: str
    lang_proba_threshold: float
    corpus_sample_ratio: float
    num_seed_word_sample: int
    google_search_num_result: int
    max_seed_url_length: int
    max_consecutive_newline: int
    total_samples: int
    total_text_pages: int
    extensions_to_exclude: List[str]
    domains_to_exclude: List[str]


@dataclass
class PipelineConfig:
    paths: Paths
    files: Files
    params: Params
