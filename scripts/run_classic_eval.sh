#!/bin/bash


# Set Variables
DATE="0000"
SAVE_PATH="data/$DATE/grade"
SAMPLE_ID_PATH="data/$DATE/sample_video_ls_0910.json"
REF_PATH="/home/bli/FunQA_eval/data/groundtruth/reference.json"
SUB_PATHS=(
    "data/$DATE/submission/test1.json"
    # Add other paths as required
)

# Loop over each submission file
for SUB_FILE in "${SUB_PATHS[@]}"; do
    python3 gpt4_eval.py $SUB_FILE $REF_PATH $SAVE_PATH $DATE
done
