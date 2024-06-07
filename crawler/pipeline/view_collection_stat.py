import hydra
from hydra.core.config_store import ConfigStore
from common_utils.config import PipelineConfig
from common_utils.utils import get_file_path
from src.collection_stat import CollectionStatistic
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

#!/usr/bin/env python
#
# view_collection_stat.py
# Gabriel de Jesus (mestregabrieldejesus@gmail.com)
# 15-07-2023


class ViewCollectionStatistic:
    """ This class shows the corpus summarization. """

    def __init__(self, cfg) -> None:
        self.collection_stat = CollectionStatistic(
            get_file_path(cfg.paths.data, cfg.files.final_corpus),
            get_file_path(cfg.paths.data, cfg.files.url_in_out_links),
            get_file_path(cfg.paths.data, cfg.files.stats_in_out_links)
        )

    def run(self) -> None:
        self.collection_stat.generate_stats()


cs = ConfigStore.instance()
cs.store(name="pipeline_config", node=PipelineConfig)
if __name__ == "__main__":
    @hydra.main(config_path="conf", config_name="config")
    def main(cfg: PipelineConfig):
        generate_stat = ViewCollectionStatistic(cfg)
        generate_stat.run()

    main()
