import yaml 

lang_codes = {
    "as": "Assamese",
    "bn": "Bengali",
    "brx": "Bodo",
    "doi": "Dogri",
    "gom": "Konkani",
    "gu": "Gujarati",
    "hi": "Hindi",
    "kn": "Kannada",
    "ks": "Kashmiri",
    "mai": "Maithili",
    "ml": "Malayalam",
    "mr": "Marathi",
    "mni": "Manipuri",
    "ne": "Nepali",
    "or": "Odia",
    "pa": "Punjabi",
    "sa": "Sanskrit",
    "sat": "Santali",
    "sd": "Sindhi",
    "ta": "Tamil",
    "te": "Telugu",
    "ur": "Urdu",
}

for direction in ["enxx", "xxen"]:
    task_list = []
    for k, v in lang_codes.items():
        config = {
            "include": f"_default_template_{direction}_yaml",
            "test_split": k,
            "task": f"in22_gen_{direction}_{k}",
        }
        task_list.append(f"in22_gen_{direction}_{k}")

        with open(f"in22_gen_{direction}_{k}.yaml", "w", encoding="utf-8") as f:
            yaml.dump(config, f, allow_unicode=True)

    with open(f"_in22_gen_{direction}.yaml", "w", encoding="utf-8") as f:
        yaml.dump(
            {
                "group": f"in22_gen_{direction}",
                "task": sorted(task_list),
                "aggregate_metric_list": [{"metric": "acc", "weight_by_size": True}],
                "metadata": {"version": 0.0}
            },
            f,
            allow_unicode=True,
        )