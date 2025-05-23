import yaml

languages = {
    "bn": "Bengali",
    "en": "English",
    "gu": "Gujarati",
    "hi": "Hindi",
    "kn": "Kannada",
    "ml": "Malayalam",
    "mr": "Marathi",
    "or": "Odia",
    "pa": "Punjabi",
    "ta": "Tamil",
    "te": "Telugu",
}

task_names = []

for lang_code, lang in languages.items():
    dict_ = {
        "dataset_name": lang_code,
        "include": "_default_template_yaml",
        "task": f"mmlu_indic_{lang}",
    }

    task_names.append(f"mmlu_indic_{lang}")

    with open(f"mmlu_indic_{lang}.yaml", "w", encoding="utf-8") as f:
        yaml.dump(dict_, f, default_flow_style=False)


main_config = {
    "group": "mmlu_indic",
    "task": task_names,
    "aggregate_metric_list": [
        {
            "metric": "acc",
            "weight_by_size": True,
        }
    ],
    "metadata": {
        "version": 0.0,
    },
}

with open("_mmlu_indic.yaml", "w", encoding="utf-8") as f:
    yaml.dump(main_config, f, default_flow_style=False)