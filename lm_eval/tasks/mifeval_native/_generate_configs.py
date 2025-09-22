import yaml 

# Custom YAML representer for handling !function tags
class FunctionTag:
    def __init__(self, value):
        self.value = value

def function_representer(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data.value, style='')

yaml.add_representer(FunctionTag, function_representer)

languages = [
    "en", "asm", "ben", "guj", "hin", "kan", "mal", "mar", "nep", "odi", "pan", "tam", "tel", "urd"
]

task_names = []
prefix = "mifeval_native"

for lang in languages:
    dict_ = {
        "task": f"{prefix}_{lang}",
        "dataset_path": "manan-u/indic-if_eval",
        "dataset_name": None,
        "output_type": "generate_until",
        "test_split": f"train_{lang}",
        "num_fewshot": 0,
        "doc_to_text": "prompt",
        "doc_to_target": 0,
        "generation_kwargs": {
            "until": [],
            "do_sample": False,
            "temperature": 0.0,
            "max_gen_toks": 1280
        },
        "process_results": FunctionTag("!function utils.process_results"),
        "metric_list": [
            {
                "metric": "prompt_level_strict_acc",
                "aggregation": "mean",
                "higher_is_better": True
            },
            {
                "metric": "inst_level_strict_acc",
                "aggregation": FunctionTag("!function utils.agg_inst_level_acc"),
                "higher_is_better": True
            },
            {
                "metric": "prompt_level_loose_acc",
                "aggregation": "mean", 
                "higher_is_better": True
            },
            {
                "metric": "inst_level_loose_acc",
                "aggregation": FunctionTag("!function utils.agg_inst_level_acc"),
                "higher_is_better": True
            }
        ],
        "metadata": {
            "version": 4.0
        }
    }

    task_names.append(f"{prefix}_{lang}")

    with open(f"{prefix}_{lang}.yaml", "w", encoding="utf-8") as f:
        content = yaml.dump(dict_, f, default_flow_style=False)
        # Post-process to fix the function tags
        with open(f"{prefix}_{lang}.yaml", "r") as rf:
            content = rf.read()
        content = content.replace("'!function ", "!function ")
        content = content.replace("'", "")
        with open(f"{prefix}_{lang}.yaml", "w") as wf:
            wf.write(content)


main_config = {
    "group": prefix,
    "task": task_names,
    "metadata": {
        "version": 4.0,
    },
}

with open(f"_{prefix}.yaml", "w", encoding="utf-8") as f:
    yaml.dump(main_config, f, default_flow_style=False)