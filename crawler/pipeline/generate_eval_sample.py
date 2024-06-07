import warnings

import hydra
from common_utils.config import PipelineConfig
from common_utils.utils import get_file_path
from hydra.core.config_store import ConfigStore
from src.get_sample_corpus import GetSampleCorpus

warnings.filterwarnings("ignore", category=UserWarning)

#!/usr/bin/env python
#
# generate_eval_sample.py
# Gabriel de Jesus (mestregabrieldejesus@gmail.com)
# 20-07-2023


class GenerateEvalSample:
    """Class for generating sample data."""

    def __init__(self, cfg) -> None:
        self.generate_eval_sample = GetSampleCorpus(
            get_file_path(cfg.paths.data, cfg.files.final_corpus),
            cfg.paths.eval_sample,
            cfg.params.total_samples,
            cfg.params.total_text_pages,
        )

    def run(self):
        try:
            self.generate_eval_sample.generate_sample()
        except ValueError as e:
            print(f"Insuficient sample: {e}")


cs = ConfigStore.instance()
cs.store(name="pipeline_config", node=PipelineConfig)
if __name__ == "__main__":

    @hydra.main(config_path="conf", config_name="config")
    def main(cfg: PipelineConfig):
        eval_samples = GenerateEvalSample(cfg)
        eval_samples.run()

    main()
