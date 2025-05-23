import yaml

languages = [
    "Bengali",
    "English",
    "Gujarati",
    "Hindi",
    "Kannada",
    "Malayalam",
    "Marathi",
    "Odia",
    "Punjabi",
    "Tamil",
    "Telugu",
]

task_names = []

for lang in languages:
    dict_ = {
        "dataset_name": lang,
        "include": "_flan_cot_template_yaml",
        "task": f"milu_{lang}",
    }

    task_names.append(f"milu_{lang}")

    with open(f"milu_{lang}.yaml", "w", encoding="utf-8") as f:
        yaml.dump(dict_, f, default_flow_style=False)


main_config = {
    "group": "milu",
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

with open("_milu.yaml", "w", encoding="utf-8") as f:
    yaml.dump(main_config, f, default_flow_style=False)
