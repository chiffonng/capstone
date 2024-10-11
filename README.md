# Mnemonic Generation for English Words

Vocabulary acquisition poses a significant challenge for language learners, particularly at medium and advanced levels, where the complexity and volume of new words can hinder retention. One promising solution is mnemonics, which leverage associations between new vocabulary and memorable cues to enhance recall. Previous efforts to automate generating these mnemonics often focus primarily on _shallow-encoding mnemonics_ (spelling or phonological features of a word) and have lower likelihood of improving retention, compared to _deep-enconding information_

This project explores an alternative approach by instruction tuning the LLaMA 3 (8B) language model on a manually curated dataset of over 1,000 examples. Unlike prior methods, this dataset includes more _deep-encoding mnemonics_ (semantic information such as morphology and etymology, associations with synonyms, antonyms, or related words and concepts). By fine-tuning the model on this diverse dataset, we aim to improve the quality and variety of mnemonics generated by the model, and improve the retention of new vocabulary for language learners.

| **Shallow-Encoding Mnemonics**                                                      | **Deep-Encoding Mnemonics**                                                                                  |
| ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **Homophonic:** olfactory sounds like "old factory."                                | **Etymology**: preposterous - pre (before) + post (after) + erous, which implies absurd.                     |
| **Chunking:** obsequious sounds like "ob-se-ki-ass. Obedient servants kiss your ass | **Morphology:** Suffixes "ate" are usually verbs. Prefix "ab" means from, away.                              |
| **Keyword:** Phony sounds like “phone-y,” which means fraudulent (phone calls).     | **Context/Story:** His actions of pouring acid on the environment are detrimental                            |
| **Rhyming:** wistful/longing for the past but wishful for the future.               | **Synonym/Antonym** "benevolent" ~ "kind" or "generous," and "malevolent" is its antonym.                    |
|                                                                                     | **Image Association:** exuberant - The ex-Uber driver never ranted; he always seems ebullient and lively.    |
|                                                                                     | **Related words**: Phantasm relates to an illusion or ghostly figure, closely tied to the synonym “phantom.” |

---

# Project components

- [ ] A web interface (using Gradio) for the tuned model.
- [ ] A dataset of 1200 examples (will be refined continually).
- [ ] This documented codebase.

# Setup

Python >= 3.10 and `requirements.txt`.
