# Can a Small Language Model learn Vietnamese like children?

## Overview

See [report](report.md) for my ongoing progress of written work.

## Installation

To experiment with reproducibility, this project uses Docker to containerize the environment. To build the Docker image, run the following command:

```bash
docker
```

## Dataset source

Aim: 2-3 million data points. All original sources used for training are listed [here](https://docs.google.com/document/d/1acj0_pxlS0813XGfy02-WtfHdhHK_apYwhI8AH8Frck/edit)

Pipeline for crawling data will use [Apache Nutch](https://nutch.apache.org/) and [Apache Solr](https://lucene.apache.org/solr/) as described in ([de Jesus & Nunes, 2024](https://aclanthology.org/2024.lrec-main.390/))'s pipeline for constructing corpus.

## TODOS

- [ ] Create a high-quality training dataset (5 million data points) for Vietnamese by crawling stories and textbooks for children (< 11 years old) and generating diverse and coherent stories by prompts.
  - Use Nutch-based tools, such as Apache Nutch and Apache Solr
  - Adapt the pipeline to generate [Cosmopedia](https://github.com/huggingface/cosmopedia)
- [ ] Train a GPT-like model on the dataset
  - [ ] Learn FlashAttention
  - [ ] Learn about ALiBi (replacing sinusoidal positional encoding)

## What I learned to finish this Capstone

1. Minitorch - [0](https://github.com/minitorch/minitorch-module-0-chiffonng) | [1](https://github.com/minitorch/minitorch-module-1-chiffonng)
2. [Natural Language Processing Specialization](https://coursera.org/verify/specialization/3FJ3W7QJX8GK)
3. CMU Advanced NLP - [Mini Llama](https://github.com/chiffonng/cmu-advanced-nlp-minllama-assignment) | [RAG system](https://github.com/chiffonng/knowledge-rag)
4. Stanford CS336 Language Modeling from Scratch
5. nanoGPT - [StanfordNLP's notebook](https://github.com/mlberkeley/learn-llm/blob/main/minGPT_student.ipynb)

```

```
