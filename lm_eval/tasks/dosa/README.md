# DOSA
DOSA is the first community-generated Dataset of 615 Social Artifacts from different Indian geographical subcultures. It was created using participatory research methods by engaging with 260 participants from 19 different Indian geographic subcultures. The dataset uses a gamified framework that relies on collective sensemaking to collect the names and descriptions of social artifacts (particularly food and cuisine) such that the descriptions semantically align with the shared sensibilities of individuals from those cultures.

Paper: \
[https://aclanthology.org/2024.lrec-main.474/](https://aclanthology.org/2024.lrec-main.474/)

### MCQ Reformulation

The DOSA dataset has been reformulated into multiple-choice question (MCQ) format for this benchmark. The clues/descriptions from the original dataset serve as questions, and three hard distractors were generated using GPT-4o to create a 4-option MCQ format alongside the correct answer.

[https://huggingface.co/datasets/pranjalchitale/dosa_mcq](https://huggingface.co/datasets/pranjalchitale/dosa_mcq)


### Task

* `dosa`: Evaluation task for DOSA MCQ benchmark

### Citation

```bibtex
@inproceedings{seth-etal-2024-dosa,
    title = "{DOSA}: A Dataset of Social Artifacts from Different {I}ndian Geographical Subcultures",
    author = "Seth, Agrima  and
      Ahuja, Sanchit  and
      Bali, Kalika  and
      Sitaram, Sunayana",
    editor = "Calzolari, Nicoletta  and
      Kan, Min-Yen  and
      Hoste, Veronique  and
      Lenci, Alessandro  and
      Sakti, Sakriani  and
      Xue, Nianwen",
    booktitle = "Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024)",
    month = may,
    year = "2024",
    address = "Torino, Italia",
    publisher = "ELRA and ICCL",
    url = "https://aclanthology.org/2024.lrec-main.474/",
    pages = "5323--5337"
}
```
