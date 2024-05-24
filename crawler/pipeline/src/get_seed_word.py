import random
from pathlib import Path
from collections import Counter
from tetuntokenizer.tokenizer import TetunWordTokenizer
from typing import List, Dict
from common_utils.tetun_lid import TetunLid
from common_utils.utils import Utils

#!/usr/bin/env python
#
# get_seed_word.py
# Gabriel de Jesus (mestregabrieldejesus@gmail.com)
# 01-07-2023


class GetSeedWords:
    """ 
    This class:
    (1) Gets a random text sample as per the predefined ratio.
    (2) Tokenizes the text sample into tokens (words).
    (3) Applies the LID model to get tokens with the probability >= threshold.
    (4) Counts the word frequency and calculates its probability of distribution.
    (5) Samples three unique words from (4) and saves them to the seed file.
    """

    def __init__(
        self,
        main_corpus_file_path: Path,
        tetun_lang: str,
        corpus_sample_ratio: float,
        lid_model_file_path: Path,
        lang_proba_threshold: float,
        num_seed_words_sample: int,
        seed_words_file_path: Path,
    ) -> None:
        self.main_corpus = Utils(main_corpus_file_path)
        self.corpus_sample_ratio = corpus_sample_ratio
        self.lid_model_file_path = lid_model_file_path
        self.lang_proba_threshold = lang_proba_threshold
        self.num_seed_words_sample = num_seed_words_sample
        self.seed_words_file = Utils(seed_words_file_path)
        self.tetun_lang = tetun_lang
        self.tetun_lid = TetunLid(
            self.tetun_lang, self.lang_proba_threshold, lid_model_file_path)

    def get_sample_corpus(self) -> List[str]:
        """
        Generates a random text sample from the corpus 
        as per the predefined ratio and return it in a list of strings.
        """

        corpus = self.main_corpus.load_corpus()

        corpus_size = len(corpus)
        sample_size = int(self.corpus_sample_ratio * corpus_size)
        sample_corpus = random.sample(corpus, sample_size)

        return sample_corpus

    def tokenize_sample_corpus(self) -> List[str]:
        """ Tokenizes the sample corpus into tokens and return them in a list of strings. """

        doc = self.get_sample_corpus()
        print(f"\nTotal corpus sample: {len(doc)} documents.")

        tokenizer = TetunWordTokenizer()
        doc_lower = str(doc).lower()
        words = tokenizer.tokenize(doc_lower)

        return words

    def calculate_proba_distribution(self) -> Dict:
        """
        Counts word frequency, calculate its probability of distribution and 
        return a dictionary contains words and their distribution probability.
        """

        # Apply the Tetun LID model to the tokenized words
        words = self.tetun_lid.get_tetun_text(self.tokenize_sample_corpus())

        freq_dict = Counter(words)
        total_words = len(words)
        probs_dist = {word: count / total_words for word,
                      count in freq_dict.items()}

        return probs_dist

    def generate_seed_words(self) -> str:
        """
        Samples three unique words and save them into the seed file 
        and return a string of sampled words.
        """

        proba_dist = self.calculate_proba_distribution()
        sequence_words = list(proba_dist.keys())
        weights = list(proba_dist.values())
        samples = set()
        while len(samples) < self.num_seed_words_sample:
            sample = random.choices(sequence_words, weights)[0]
            samples.add(sample)
            sequence_words.remove(sample)
            weights.remove(proba_dist[sample])

        seeds = " ".join(list(samples))
        self.seed_words_file.save_corpus(seeds)
        print(f"Seed words: {seeds}")

        return seeds
