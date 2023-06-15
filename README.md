# FunQA: Towards Surprising Video Comprehension

[Blog]() (coming soon) | [Paper]() (coming soon)

[![Youtube](https://badges.aleen42.com/src/youtube.svg)]()
[![Arxiv]()]()
[![Bilibili](https://img.shields.io/badge/Bilibili-Watch-pink)]()
[![HumorQA_Demo](https://img.shields.io/badge/HumorQA_Demo-Watch-green)]()
[![CreativeQA_Demo](https://img.shields.io/badge/CreativeQA_Demo-Watch-blue)]()
[![MagicQA_Demo](https://img.shields.io/badge/MagicQA_Demo-Watch-orange)]()


![img.png](img/main.png)

Welcome to FunQA's open source repository, FunQA is a Video Question Answering benchmark that aims
at enhancing video reasoning upon counter-intuitive videos, such as humorous
videos, creative videos, and magic videos.

This repository is still under maintenance and we will update the full FunQA dataset and our model in the future.



## Todo

1. [x] Release the FunQA dataset.
1. [x] Post the paper: FunQA: Towards Surprising Video Comprehension
2. [ ] Release the FunQA Extended dataset.
3. [ ] Release our full benchmark, comparison results with other LLMs and the new metrics for Free-text task.

## Table of Contents

- [FunQA Benchmark](#funqa-benchmark)
    * [FunQA Dataset Construction and Tasks](#funqa-dataset-construction-and-tasks)
    * [FunQA Extension Dataset](#funqa-extension-dataset)
    * [Dataset Examples](#dataset-examples)
- [Data Preparation](#data-preparation)
- [Acknowledgement](#acknowledgement)
- [License](#license)

## FunQA Benchmark

- FunQA is a pioneering **VideoQA benchmark** specially curated to hone video reasoning capabilities in the
  counter-intuitive context of **humorous**, **creative**, and **magic** videos.
- We create FunQA with the principle of **spatial-temporal**, **visual-centric reasoning**, and **Free-text generation**. Rigorous
  tasks including **positioning**, **describing**, and **reasoning** the counter-intuitive clips are set up.
- FunQA dataset has a total of 4.3k videos, 23.9 hours, and a total of 312k QA pairs with high quality.

### Dataset Construction and Tasks

### Dataset Statics
FunQA contains **4,365** counter-intuitive video clips and **311,950** question-answer pairs, the total
length of these videos is **23.9** hours and the average length of video clips is **19** seconds.
### Extension Dataset

#### FunQA Multi-choice Dataset

![FunQA_MC.png](img/FunQA_MC.png)

#### FunQA Dialog Dataset
![img_1.png](img/FunQA_dia.png)

### Dataset Examples

## Install

You can create an anaconda environment for this project

```angular2html
conda create -n funqa python==3.8
conda activate videoqa
git clone https://github.com/Jingkang50/FunQA
```

## Data Preparation

Please download all the videos and annotation files from [here]().

For FunQA Dataset: there are four zip files:

- `funqa_train.zip`, `funqa_val.zip`, `funqa_test.zip`: Videos for training, validation and test.
- `funqa_base_annotation.zip`: Annotation files for FunQA Base Dataset.
  After downloading, please unzip `funqa_train.zip`, `funqa_val.zip` and `funqa_test.zip` to a folder called
  `funqa_base\videos` and unzip `funqa_base_annotation.zip` to a folder called `funqa_base\annotation`.

For FunQA Extension Dataset: Coming soon.

## Results
## Acknowledgement

This study is supported by the Ministry of Education, Singapore, under its MOE AcRF Tier 2 (MOE-T2EP20221- 0012), NTU
NAP, and under the RIE2020 Industry Alignment Fund – Industry Collaboration Projects (IAF-ICP) Funding Initiative, as
well as cash and in-kind contribution from the industry partner(s).

## License