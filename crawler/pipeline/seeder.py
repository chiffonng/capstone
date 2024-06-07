import warnings

import hydra
from common_utils.config import PipelineConfig
from common_utils.utils import get_file_path
from hydra.core.config_store import ConfigStore
from src.get_seed_url import GetSeedUrl
from src.get_seed_word import GetSeedWords

warnings.filterwarnings("ignore", category=UserWarning)

#!/usr/bin/env python
#
# seeder.py
# Gabriel de Jesus (mestregabrieldejesus@gmail.com)
# 01-07-2023


class MainSeeder:
    """This class generates seed words and seed URLs, including domains from the seed URLs."""

    def __init__(self, cfg) -> None:
        self.get_seed_word = GetSeedWords(
            get_file_path(cfg.paths.data, cfg.files.main_corpus),
            cfg.params.language,
            cfg.params.corpus_sample_ratio,
            get_file_path(cfg.paths.lid, cfg.files.lid_model),
            cfg.params.lang_proba_threshold,
            cfg.params.num_seed_word_sample,
            get_file_path(cfg.paths.data, cfg.files.seed_words),
        )
        self.get_url = GetSeedUrl(
            cfg.params.extensions_to_exclude,
            cfg.params.domains_to_exclude,
            self.get_seed_word.generate_seed_words(),
            cfg.params.google_search_num_result,
            cfg.params.max_seed_url_length,
            get_file_path(cfg.paths.nutch, cfg.files.nutch_seed_url),
            get_file_path(cfg.paths.data, cfg.files.domain),
        )

    def run(self) -> None:
        try:
            self.get_url.generate_seed_urls()
            print(f"\nSeed URLs have been generated successfully.\n\n")
        except Exception as e:
            print(f"\nError while generating the seed URLs: {e}\n")


cs = ConfigStore.instance()
cs.store(name="pipeline_config", node=PipelineConfig)
if __name__ == "__main__":

    @hydra.main(config_path="conf", config_name="config")
    def main(cfg: PipelineConfig):
        seeder = MainSeeder(cfg)
        seeder.run()

    main()
