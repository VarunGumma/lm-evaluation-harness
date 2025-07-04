bash run.sh mmlu mmlu
bash run.sh mmlu_indic mmlu_indic
bash run.sh mmlu_indic_roman mmlu_indic_roman

bash run.sh igb/xsum igb_xsum
bash run.sh igb/xorqa igb_xorqa
bash run.sh igb/xquad igb_xquad
bash run.sh igb/flores_xxen igb_flores_xxen
bash run.sh igb/flores_enxx igb_flores_enxx

bash run.sh milu milu
bash run.sh triviaqa_indic_mcq triviaqa_indic_mcq
bash run.sh arc_c_indic arc_c_indic
bash run.sh boolq_indic boolq_indic

## rm -rf /datadisk/storage/varunartifacts/containers/indic-phi/checkpoints/evaluations
# cp -r evaluations /datadisk/storage/varunartifacts/containers/indic-phi/checkpoints