export NCCL_SOCKET_IFNAME=lo
export NCCL_DEBUG=WARN

ckpt_dir="/datadisk/storage/varunartifacts/containers/indic-phi/checkpoints/models"
results_dir="evaluations/igb/xquad"
task_name="igb_xquad"

rm -rf logs ${results_dir}
mkdir -p logs ${results_dir}

# Load from Checkpoint
for ckpt in $(ls $ckpt_dir); do
    for model in $(ls $ckpt_dir/$ckpt); do
        echo " | > checkpoint: $ckpt | model: $model"
        bash dp.sh ${ckpt_dir}/${ckpt}/${model}/checkpoint-best $results_dir $task_name > logs/${model}_${ckpt}.log 2>&1
    done
done

# HF Baselines
bash dp.sh "krutrim-ai-labs/Krutrim-2-instruct" $results_dir $task_name > logs/krutrim_2.log 2>&1

bash dp.sh "meta-llama/Llama-3.2-1B-Instruct" $results_dir $task_name > logs/llama_3.2_3b.log 2>&1
bash dp.sh "meta-llama/Llama-3.2-3B-Instruct" $results_dir $task_name > logs/llama_3.2_3b.log 2>&1
bash dp.sh "meta-llama/Llama-3.1-8B-Instruct" $results_dir $task_name > logs/llama_3.1_8b.log 2>&1
bash dp.sh "meta-llama/Llama-3.3-70B-Instruct" $results_dir $task_name > logs/llama_3.3_70b.log 2>&1
# bash dp_mp.sh "meta-llama/Llama-3.1-405B-Instruct" $results_dir $task_name > logs/llama_3.1_405b.log 2>&1

bash dp.sh "google/gemma-3-1b-it" $results_dir $task_name > logs/gemma_3_1b.log 2>&1
bash dp.sh "google/gemma-3-4b-it" $results_dir $task_name > logs/gemma_3_4b.log 2>&1
bash dp.sh "google/gemma-3-12b-it" $results_dir $task_name > logs/gemma_3_12b.log 2>&1
bash dp.sh "google/gemma-3-27b-it" $results_dir $task_name > logs/gemma_3_27b.log 2>&1

bash dp.sh "microsoft/phi-4-mini-instruct" $results_dir $task_name > logs/phi_4_mini_instruct.log 2>&1
bash dp.sh "microsoft/phi-4" $results_dir $task_name > logs/phi_4.log 2>&1

bash dp.sh "CohereLabs/aya-expanse-8b" $results_dir $task_name > logs/aya_expanse_8b.log 2>&1
bash dp.sh "CohereLabs/aya-expanse-32b" $results_dir $task_name > logs/aya_expanse_32b.log 2>&1