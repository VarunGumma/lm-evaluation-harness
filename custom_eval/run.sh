export NCCL_SOCKET_IFNAME=lo
export NCCL_DEBUG=WARN
export TRANSFORMERS_VERBOSITY=error

sub_dir=$1
task_name=$2

results_dir="/scratch/amlt_code/evaluations/${sub_dir}"
logs_dir="/scratch/amlt_code/logs/${sub_dir}"
ckpt_dir="/datadisk/storage/varunartifacts/containers/indic-phi/checkpoints/models"

rm -rf ${logs_dir}
mkdir -p ${logs_dir} ${results_dir}

# Load from Checkpoint
for ckpt in $(ls $ckpt_dir); do
    for model in $(ls $ckpt_dir/$ckpt); do
        echo " | > Running model: ${ckpt_dir}/${ckpt}/${model} on task: ${task_name}"
        bash dp.sh "${ckpt_dir}/${ckpt}/${model}/checkpoint-best" ${results_dir} $task_name \
            > ${logs_dir}/${model}_${ckpt}.log 2>&1
    done
done

# HF Baselines
echo " | > Running model: krutrim-ai-labs/Krutrim-2-instruct on task: ${task_name}"
bash dp.sh "krutrim-ai-labs/Krutrim-2-instruct" ${results_dir} $task_name \
    > ${logs_dir}/krutrim_2.log 2>&1

echo " | > Running model: meta-llama/Llama-3.2-1B-Instruct on task: ${task_name}"
bash dp.sh "meta-llama/Llama-3.2-1B-Instruct" ${results_dir} $task_name \
    > ${logs_dir}/llama_3.2_1b.log 2>&1

echo " | > Running model: meta-llama/Llama-3.2-3B-Instruct on task: ${task_name}"
bash dp.sh "meta-llama/Llama-3.2-3B-Instruct" ${results_dir} $task_name \
    > ${logs_dir}/llama_3.2_3b.log 2>&1

echo " | > Running model: meta-llama/Llama-3.1-8B-Instruct on task: ${task_name}"
bash dp.sh "meta-llama/Llama-3.1-8B-Instruct" ${results_dir} $task_name \
    > ${logs_dir}/llama_3.1_8b.log 2>&1

echo " | > Running model: meta-llama/Llama-3.3-70B-Instruct on task: ${task_name}"
bash dp.sh "meta-llama/Llama-3.3-70B-Instruct" ${results_dir} $task_name \
    > ${logs_dir}/llama_3.3_70b.log 2>&1

# echo " | > Running model: meta-llama/Llama-3.1-405B-Instruct on task: ${task_name}"
# bash dp_mp.sh "meta-llama/Llama-3.1-405B-Instruct" ${results_dir} $task_name \
#     > ${logs_dir}/llama_3.1_405b.log 2>&1

echo " | > Running model: google/gemma-3-1b-it on task: ${task_name}"
bash dp.sh "google/gemma-3-1b-it" ${results_dir} $task_name \
    > ${logs_dir}/gemma_3_1b.log 2>&1

echo " | > Running model: google/gemma-3-4b-it on task: ${task_name}"
bash dp.sh "google/gemma-3-4b-it" ${results_dir} $task_name \
    > ${logs_dir}/gemma_3_4b.log 2>&1

echo " | > Running model: google/gemma-3-12b-it on task: ${task_name}"
bash dp.sh "google/gemma-3-12b-it" ${results_dir} $task_name \
    > ${logs_dir}/gemma_3_12b.log 2>&1

echo " | > Running model: google/gemma-3-27b-it on task: ${task_name}"
bash dp.sh "google/gemma-3-27b-it" ${results_dir} $task_name \
    > ${logs_dir}/gemma_3_27b.log 2>&1

echo " | > Running model: microsoft/phi-4-mini-instruct on task: ${task_name}"
bash dp.sh "microsoft/phi-4-mini-instruct" ${results_dir} $task_name \
    > ${logs_dir}/phi_4_mini_instruct.log 2>&1

echo " | > Running model: microsoft/phi-4 on task: ${task_name}"
bash dp.sh "microsoft/phi-4" ${results_dir} $task_name \
    > ${logs_dir}/phi_4.log 2>&1

echo " | > Running model: CohereLabs/aya-expanse-8b on task: ${task_name}"
bash dp.sh "CohereLabs/aya-expanse-8b" ${results_dir} $task_name \
    > ${logs_dir}/aya_expanse_8b.log 2>&1

echo " | > Running model: CohereLabs/aya-expanse-32b on task: ${task_name}"
bash dp.sh "CohereLabs/aya-expanse-32b" ${results_dir} $task_name \
    > ${logs_dir}/aya_expanse_32b.log 2>&1

echo " | > Running model: VarunGumma/Mistral-Small-3.1-24B-Instruct-2503-LM-HF on task: ${task_name}"
bash dp.sh "VarunGumma/Mistral-Small-3.1-24B-Instruct-2503-LM-HF" ${results_dir} $task_name \
    > ${logs_dir}/mistral_small_3.1_24b.log 2>&1

echo " | > Running model: sarvamai/sarvam-m on task: ${task_name}"
bash dp.sh "sarvamai/sarvam-m" ${results_dir} $task_name \
    > ${logs_dir}/sarvam_m.log 2>&1