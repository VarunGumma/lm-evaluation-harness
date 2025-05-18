CKPT_DIR=$1
OUTPUT_DIR=$2

mkdir -p ${OUTPUT_DIR}

accelerate launch -m lm_eval \
    --model hf \
    --model_args "pretrained=${CKPT_DIR},parallelize=False,dtype=bfloat16,attn_implementation=flash_attention_2" \
    --output_path ${OUTPUT_DIR} \
    --apply_chat_template \
    --batch_size 24 \
    --tasks milu-core \
    --log_samples