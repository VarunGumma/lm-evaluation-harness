# m-IFeval (Multilingual Instruction Following Evaluation)

m-IFeval is a multilingual extension of the IFeval task, which evaluates a model's ability to follow instructions. This implementation uses the translated version of IFeval available at [manan-u/ifeval-translated](https://huggingface.co/datasets/manan-u/ifeval-translated).

## Dataset

The dataset contains IFeval translated into multiple languages with splits named as `train_{lang_code}`. Each language contains 541 examples.

### Available Languages

- **en**: English
- **asm**: Assamese  
- **ben**: Bengali
- **guj**: Gujarati
- **hin**: Hindi
- **kan**: Kannada
- **mal**: Malayalam
- **mar**: Marathi
- **nep**: Nepali
- **odi**: Odia
- **pan**: Punjabi
- **tam**: Tamil
- **tel**: Telugu
- **urd**: Urdu

## Usage

### Evaluate a single language
```bash
lm_eval --model hf --model_args pretrained=model_name --tasks mifeval_en
```

### Evaluate all languages
```bash
lm_eval --model hf --model_args pretrained=model_name --tasks mifeval
```

### Evaluate specific languages
```bash
lm_eval --model hf --model_args pretrained=model_name --tasks mifeval_hin,mifeval_ben,mifeval_tam
```

## Metrics

The evaluation provides both strict and loose accuracy metrics:

- **prompt_level_strict_acc**: Strict accuracy at the prompt level (all instructions must be followed)
- **inst_level_strict_acc**: Strict accuracy at the instruction level
- **prompt_level_loose_acc**: Loose accuracy at the prompt level
- **inst_level_loose_acc**: Loose accuracy at the instruction level

## Implementation Details

- **Version**: 4.0
- **Base Task**: IFeval
- **Dataset Source**: manan-u/ifeval-translated
- **Evaluation Type**: Generation-based
- **Max Generation Tokens**: 1280
- **Temperature**: 0.0
- **Few-shot Examples**: 0

## Citation

This task builds upon the original IFeval paper. If you use this multilingual version, please cite both the original IFeval work and acknowledge the translation effort.