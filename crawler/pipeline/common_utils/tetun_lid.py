import os
import joblib
from typing import List
from pathlib import Path

#!/usr/bin/env python
#
# tetun_lid.py
# Gabriel de Jesus (mestregabrieldejesus@gmail.com)
# 20-06-2023


class TetunLid:
    """
    Tetun LID class loads the LID model file, applies it to the input text, 
    and then filters out texts that do not meet the predefined threshold.
    """

    def __init__(
        self, tetun_lang: str, lang_proba_threshold: float, lid_model_file_path: str,
    ) -> None:
        self.tetun_lang = tetun_lang
        self.lang_proba_threshold = lang_proba_threshold
        self.lid_model_file_path = lid_model_file_path

    def load_lid_model(self) -> object:
        """ Loads  and return the language identification (LID) model. """

        if not os.path.exists(self.lid_model_file_path):
            print(f"Model file not found at: {self.lid_model_file_path}")
            return []
        model = joblib.load(Path(self.lid_model_file_path))

        return model

    def get_tetun_text(self, input_text: List[str]) -> List[str]:
        """
        Gets Tetun words with a probability >= threshold. 

        :param input_text: a list of string.
        :return: a list of texts.
        """

        tetun_text = []
        tetun_lid_model = self.load_lid_model()
        pred_probs = tetun_lid_model.predict_proba(input_text)
        for i, probs in enumerate(pred_probs):
            for j, lang in enumerate(tetun_lid_model.classes_):
                if lang == self.tetun_lang and round(probs[j], 2) >= self.lang_proba_threshold:
                    tetun_text.append(input_text[i])

        return tetun_text
