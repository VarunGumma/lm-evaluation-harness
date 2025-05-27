import yaml 

languages = [
    "bn", "en", "gu", "hi", "kn", "ml", "mr", "or", "pa", "ta", "te"
]

task_names = []
prefix = "arc_c_indic"

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
