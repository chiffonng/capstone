import hydra
from hydra.core.config_store import ConfigStore
from common_utils.config import PipelineConfig
from common_utils.utils import get_file_path
from src.get_corpus import GetCorpus
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

#!/usr/bin/env python
#
# construct_corpus.py
# Gabriel de Jesus (mestregabrieldejesus@gmail.com)
# 10-07-2023


class ConstructCorpus:
    """ This class generates text pages for the Tetun corpus and save them in a file. """

    def __init__(self, cfg) -> None:
        self.get_corpus = GetCorpus(
            cfg.params.solr_api_url,
            cfg.params.solr_start,
            cfg.params.solr_rows,
            cfg.params.max_consecutive_newline,
            cfg.params.language,
            cfg.params.lang_proba_threshold,
            get_file_path(cfg.paths.lid, cfg.files.lid_model),
            get_file_path(cfg.paths.data, cfg.files.final_corpus)
        )

    def run(self) -> None:
        try:
            self.get_corpus.generate_corpus()
            print("\nThe final corpus has been generated sucessfully.\n\n")
        except Exception as e:
            print(f"\nError while generating the final corpus: {e}\n")


cs = ConfigStore.instance()
cs.store(name="pipeline_config", node=PipelineConfig)
if __name__ == "__main__":
    @hydra.main(config_path="conf", config_name="config")
    def main(cfg: PipelineConfig):
        construct_corpus = ConstructCorpus(cfg)
        construct_corpus.run()

    main()
