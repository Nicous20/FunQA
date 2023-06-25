# [FunQA: Towards Surprising Video Comprehension](https://funqa-benchmark.github.io/)



[![paper](https://img.shields.io/badge/cs.CV-xxxx.xxxxx-b31b1b?logo=arxiv&logoColor=red)](https://arxiv.org/abs/xxx.xxxxx)
[![page](https://img.shields.io/badge/Project_Page-FunQA-orange)](https://arxiv.org/abs/xxx.xxxxx)
[![Dataset](https://img.shields.io/badge/Dataset-Download-blue)](https://drive.google.com/drive/folders/1hUjV7z_RDnGwhux663yG8-QD7WyyMnEB?usp=sharing) 
[![Youtube](https://badges.aleen42.com/src/youtube.svg)](https://youtu.be/69Mvz_k7_Z4)
[![Bilibili](https://img.shields.io/badge/Bilibili-Watch-pink)](https://www.bilibili.com/video/BV1Ch411N7bD/?share_source=copy_web&vd_source=dbe610f9a7910f3eae7ae2bf5aa6a8e2)
</br>
[![HumorQA_Demo](https://img.shields.io/badge/HumorQA_Demo-Watch-green)]()
[![CreativeQA_Demo](https://img.shields.io/badge/CreativeQA_Demo-Watch-blue)]()
[![MagicQA_Demo](https://img.shields.io/badge/MagicQA_Demo-Watch-orange)]()

Welcome to FunQA's Codebase Repository!
The motivation for the FunQA is straightforward: Humans enjoy surprising videos, including funny clips, creative performances, or visual illusions. We hope to test or emdow the similar power for AI models.

FunQA is a VideoQA dataset to evaluate and enhance the model's video reasoning capability upon counter-intuitive videos, including humorous and funny viral videos from [TikTok](), creative performance from [Kasou Taishou (欽ちゃん＆香取慎吾の全日本仮装大賞)](https://en.wikipedia.org/wiki/Kasou_Taishou), and magic videos from [YouTube]() and [TikTok]().

We establish rigorous QA tasks designed to assess the model's capability in counter-intuitive timestamp localization, detailed video description, and reasoning around counter-intuitiveness. We also pose higher-level tasks, such as attributing a fitting and vivid title to the video, and scoring the video creativity.

In total, the FunQA benchmark consists of 312K free-text QA pairs derived from 4.3K video clips, spanning a total of 24 video hours.
Extensive experiments with existing VideoQA models reveal significant performance gaps for the FunQA videos across spatial-temporal reasoning, visual-centered reasoning, and free-text generation.

<video controls>
  <source src="[https://user-images.githubusercontent.com/91806420/248528017-8872edf5-c284-405c-aa3a-8f235fb2c03c.mp4](https://github.com/OpenGVLab/Ask-Anything/assets/24236723/a8667e87-49dd-4fc8-a620-3e408c058e26)" type="video/mp4">
Your browser does not support the video tag.
</video>

## Todo

1. [x] Release the FunQA dataset and arXiv paper.
2. [ ] Release the FunQA Extended dataset.
3. [ ] Release evaluation code.

## Table of Contents

- [1. FunQA Benchmark](#funqa-benchmark)
    * [1.1 FunQA Dataset Construction and Tasks](#funqa-dataset-construction-and-tasks)
    * [1.2 FunQA Extension Dataset](#funqa-extension-dataset)
    * [1.3 Dataset Examples](#dataset-examples)
- [2. Data Preparation](#data-preparation)
- [3. Acknowledgement](#acknowledgement)
- [4. License](#license)

## 1 - FunQA Benchmark

### 1.1 - FunQA Main Tasks
![img.png](img/main.png)

### 1.2 - FunQA Extended Tasks

#### FunQA Multi-choice Dataset

![FunQA_MC.png](img/FunQA_MC.png)

#### FunQA Dialog Dataset
![img_1.png](img/FunQA_dia.png)


## 2 - Data Preparation

Please download all the videos and annotation files from [here](https://drive.google.com/drive/folders/1hUjV7z_RDnGwhux663yG8-QD7WyyMnEB?usp=sharing).

For FunQA Dataset: there are four zip files:

- `funqa_train.zip`, `funqa_val.zip`, `funqa_test.zip`: Videos for training, validation and test.
- `funqa_base_annotation.zip`: Annotation files for FunQA Base Dataset.
  After downloading, please unzip `funqa_train.zip`, `funqa_val.zip` and `funqa_test.zip` to a folder called
  `funqa_base\videos` and unzip `funqa_base_annotation.zip` to a folder called `funqa_base\annotation`.

For FunQA Extension Dataset: Coming soon.

## Acknowledgement

This study is supported by the Ministry of Education, Singapore, under its MOE AcRF Tier 2 (MOE-T2EP20221- 0012), NTU
NAP, and under the RIE2020 Industry Alignment Fund – Industry Collaboration Projects (IAF-ICP) Funding Initiative, as
well as cash and in-kind contribution from the industry partner(s).

If you're using FunQA in your research or applications, please cite using this BibTeX:
```bibtex
    @article{xie2023funqa,
      title={FunQA: Towards Surprising Video Comprehension},
      author={Xie, Binzhu and Zhang, Sicheng and Zhou, Zitang and Li, Bo and Zhang, Yuanhan and Hessel, Jack and Yang, Jingkang and Liu, Ziwei},
      journal={GitHub repository},
      year={2023},
      howpublished = {\url{https://github.com/Jingkang50/FunQA}}
  }
```

## License
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/80x15.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.


Looking forward to your feedback and please raise any issues or questions [here](https://github.com/Jingkang50/FunQA/issues). 
