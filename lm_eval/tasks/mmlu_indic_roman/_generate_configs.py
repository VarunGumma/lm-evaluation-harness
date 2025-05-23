import yaml

languages = {
    "bn": "Bengali",
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
    task_name = f"mmlu_indic_{lang}_roman"
    dict_ = {
        "dataset_name": f"{lang_code}_roman",
        "include": "_default_template_yaml",
        "task": task_name,
    }

    task_names.append(task_name)

    with open(f"{task_name}.yaml", "w", encoding="utf-8") as f:
        yaml.dump(dict_, f, default_flow_style=False)


main_config = {
    "group": "mmlu_indic_roman",
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

with open("_mmlu_indic_roman.yaml", "w", encoding="utf-8") as f:
    yaml.dump(main_config, f, default_flow_style=False)