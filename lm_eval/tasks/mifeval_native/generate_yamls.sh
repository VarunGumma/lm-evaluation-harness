#!/bin/bash

languages=("en" "asm" "ben" "guj" "hin" "kan" "mal" "mar" "nep" "odi" "pan" "tam" "tel" "urd")

for lang in "${languages[@]}"; do
    cat > "mifeval_${lang}.yaml" << EOF
task: mifeval_${lang}
dataset_path: manan-u/ifeval-translated
dataset_name: null
output_type: generate_until
test_split: train_${lang}
num_fewshot: 0
doc_to_text: prompt
doc_to_target: 0
generation_kwargs:
  until: []
  do_sample: false
  temperature: 0.0
  max_gen_toks: 1280
process_results: !function utils.process_results
metric_list:
  - metric: prompt_level_strict_acc
    aggregation: mean
    higher_is_better: true
  - metric: inst_level_strict_acc
    aggregation: !function utils.agg_inst_level_acc
    higher_is_better: true
  - metric: prompt_level_loose_acc
    aggregation: mean
    higher_is_better: true
  - metric: inst_level_loose_acc
    aggregation: !function utils.agg_inst_level_acc
    higher_is_better: true
metadata:
  version: 4.0
EOF
done

# Create the main group file
cat > "_mifeval.yaml" << EOF
group: mifeval
task:
$(for lang in "${languages[@]}"; do echo "  - mifeval_${lang}"; done)
metadata:
  version: 4.0
EOF