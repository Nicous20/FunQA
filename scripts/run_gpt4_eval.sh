#!/bin/bash

OPENAI_KEY=""

# Set Variables
DATE="0000"
GRADE_PATH="data/$DATE/grade"
OUTPUT_PATH="data/$DATE/output"
SAMPLE_ID_PATH="data/$DATE/sample_video_ls.json"
REF_PATH="data/gt/reference.json"
SUB_PATHS=(
    "data/$DATE/submission/test1.json"
    # Add other paths as required
)

# Loop over each submission file
for SUB_FILE in "${SUB_PATHS[@]}"; do
    python3 gpt4_eval.py $SUB_FILE $REF_PATH $SAMPLE_ID_PATH $GRADE_PATH $OUTPUT_PATH $DATE $OPENAI_KEY
done
