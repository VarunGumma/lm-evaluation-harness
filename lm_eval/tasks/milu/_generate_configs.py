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
prefix = "milu"

for lang in languages:
    dict_ = {
        "dataset_name": lang,
        "include": "_default_template_yaml",
        "task": f"{prefix}_{lang}",
    }

    task_names.append(f"{prefix}_{lang}")

    with open(f"{prefix}_{lang}.yaml", "w", encoding="utf-8") as f:
        yaml.dump(dict_, f, default_flow_style=False)


main_config = {
    "group": prefix,
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

with open(f"_{prefix}.yaml", "w", encoding="utf-8") as f:
    yaml.dump(main_config, f, default_flow_style=False)
