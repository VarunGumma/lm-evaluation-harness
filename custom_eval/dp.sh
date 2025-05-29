CKPT_DIR=$1
OUTPUT_DIR=$2
TASK_NAME=$3

# get the full output path by replacing the '/' in the checkpoint directory with '__'
FULL_OUTPUT_DIR=${OUTPUT_DIR}/$(echo ${CKPT_DIR} | sed 's/\//__/g')

# check it full output directory exists and is non empty
if [ -d "${FULL_OUTPUT_DIR}" ] && [ "$(ls -A ${FULL_OUTPUT_DIR})" ]; then
    echo " | > ${FULL_OUTPUT_DIR} already exists and is not empty. Exiting..."
    exit 1
fi

mkdir -p ${OUTPUT_DIR}

accelerate launch \
    -m lm_eval \
    --model hf \
    --model_args "pretrained=${CKPT_DIR},parallelize=False,dtype=bfloat16,attn_implementation=sdpa" \
    --output_path ${OUTPUT_DIR} \
    --apply_chat_template \
    --batch_size auto:40 \
    --tasks ${TASK_NAME} \
    --log_samples 