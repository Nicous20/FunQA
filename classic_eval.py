from pycocoevalcap.cider.cider import Cider
from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge import Rouge
from nltk.translate.meteor_score import meteor_score
import nltk
import pandas as pd
from tqdm import tqdm
# nltk.download('wordnet')
import os
import time
import openai
import json
import re
import sys


def calculate_bleu4(reference, hypothesis):

    ref_tokens = reference.split()
    hyp_tokens = hypothesis.split()
    blue4_score = sentence_bleu([ref_tokens],
                                hyp_tokens,
                                weights=(0.25, 0.25, 0.25, 0.25),
                                smoothing_function=SmoothingFunction().method1)

    return blue4_score


def calculate_rouge(reference, hypothesis):
    rouge = Rouge()
    rouge_score = rouge.get_scores(hypothesis, reference, avg=True)
    return rouge_score['rouge-l']['f']


def compute_cider_score(reference, candidate):
    gts = {}
    res = {}
    for idx in range(len(reference)):
        gts[idx] = [reference[idx]]
        res[idx] = [candidate[idx]]

    cider_scorer = Cider()

    cider_score, _ = cider_scorer.compute_score(gts, res)
    return cider_score
def chk_file(submission_file, answer_file):
    with open(submission_file) as f:
        submission = json.load(f)
    with open(answer_file) as f:
        answer = json.load(f)

    chk_answer = []
    for data in answer:
        chk_answer.append({
            'task': data['task'],
            'visual_input': data['visual_input'],
            'ID': data['ID']
        })

    diff = False
    for data in submission:
        if {
            'task': data['task'],
            'visual_input': data['visual_input'],
            'ID': data['ID']
        } not in chk_answer:
            print(data)
            diff = True
            break

    assert not diff, 'Submission file is not valid'
    print('File is valid! Loading File...')

    submission = sorted(submission, key=lambda x: x['ID'])
    answer = sorted(answer, key=lambda x: x['ID'])


    submission = sorted(submission, key=lambda x: x['ID'])
    answer = sorted(answer, key=lambda x: x['ID'])

    duplicate_id_output = set()


    for sub_data in submission:
        for ans_data in answer:
            if sub_data['ID'] == ans_data['ID'] and sub_data['output'] == ans_data['output']:
                duplicate_id_output.add((sub_data['ID'], sub_data['output']))


    filtered_submission = [data for data in submission if (data['ID'], data['output']) not in duplicate_id_output]
    filtered_answer = [data for data in answer if (data['ID'], data['output']) not in duplicate_id_output]

   
    submission = filtered_submission
    answer = filtered_answer
    submission = sorted(submission, key=lambda x: x['ID'])
    answer = sorted(answer, key=lambda x: x['ID'])
    print('submission: ',len(submission),'answer: ',len(answer))
    return submission,answer

def eval(submission_file, answer_file, total_score_path, run_time):
    print('Validating...')
    col = ['Task', 'H2', 'H3', 'H4', 'C2', 'C3', 'C4', 'M2', 'M3']
    chk_file(submission_file, answer_file)


    can_path = 'bleurt/test_data/candidates'
    ref_path = 'bleurt/test_data/references'
    with open(can_path, 'w') as f_can:
        f_can.close()
    with open(ref_path, 'w') as f_ref:
        f_ref.close()

    bleurt_score_path = 'score.txt'
    eval_csv = pd.DataFrame(
        columns=['pre_output', 'gt', 'Task', 'bleurt_score'])
    for i in tqdm(range(len(submission))):
        pre_output = submission[i]['output'].replace('\n', ' ')
        gt = answer[i]['output'].replace('\n', ' ')

        with open(can_path, 'a') as f_can:
            f_can.write(pre_output + '\n')
        with open(ref_path, 'a') as f_ref:
            f_ref.write(gt + '\n')
        task = answer[i]['task']
        eval_csv = pd.concat([
            eval_csv,
            pd.DataFrame([[pre_output, gt, task, 0]],
                         columns=['pre_output', 'gt', 'Task', 'bleurt_score'])
        ])

    f_can.close()
    f_ref.close()

    os.system(
        'python -m bleurt.score_files   -candidate_file={}  -reference_file={}   -bleurt_checkpoint=BLEURT-20   -scores_file={}'
        .format(can_path, ref_path, bleurt_score_path))

    from time import sleep
    sleep(run_time)

    with open(bleurt_score_path) as f:
        eval_csv['bleurt_score'] = [i[:-1] for i in f.readlines()]

    rouge_score, bleu_score, bleurt_score, cider_score = {}, {}, {}, {}
    bleurt_score['H2'], bleurt_score['H3'], bleurt_score['H4'], bleurt_score[
        'C2'], bleurt_score['C3'], bleurt_score['C4'], bleurt_score[
            'M2'], bleurt_score['M3'] = [], [], [], [], [], [], [], []
    rouge_score['H2'], rouge_score['H3'], rouge_score['H4'], rouge_score[
        'C2'], rouge_score['C3'], rouge_score['C4'], rouge_score[
            'M2'], rouge_score['M3'] = [], [], [], [], [], [], [], []
    bleu_score['H2'], bleu_score['H3'], bleu_score['H4'], bleu_score[
        'C2'], bleu_score['C3'], bleu_score['C4'], bleu_score[
            'M2'], bleu_score['M3'] = [], [], [], [], [], [], [], []

    for index, row in eval_csv.iterrows():

        if row['pre_output'] == '':
            bleu_s = 0.
            rouge_s = 0.
            bleurt_s = 0.
        else:
            groudtruth_value = str(row['gt'])
            groudtruth_value.lower()
            result_value = str(row['pre_output'])
            result_value.lower()

            bleu_s = calculate_bleu4(groudtruth_value, result_value)
            rouge_s = calculate_rouge(groudtruth_value, result_value)
            bleurt_s = float(row['bleurt_score'])

        if row['Task'][0] == 'H':
            if row['Task'][-1] == '2':
                bleu_score['H2'].append(bleu_s)
                rouge_score['H2'].append(rouge_s)
                bleurt_score['H2'].append(bleurt_s)
            elif row['Task'][-1] == '3':
                bleu_score['H3'].append(bleu_s)
                rouge_score['H3'].append(rouge_s)
                bleurt_score['H3'].append(bleurt_s)
            elif row['Task'][-1] == '4':
                bleu_score['H4'].append(bleu_s)
                rouge_score['H4'].append(rouge_s)
                bleurt_score['H4'].append(bleurt_s)

        elif row['Task'][0] == 'C':
            if row['Task'][-1] == '2':
                bleu_score['C2'].append(bleu_s)
                rouge_score['C2'].append(rouge_s)
                bleurt_score['C2'].append(bleurt_s)
            elif row['Task'][-1] == '3':
                bleu_score['C3'].append(bleu_s)
                rouge_score['C3'].append(rouge_s)
                bleurt_score['C3'].append(bleurt_s)
            elif row['Task'][-1] == '4':
                bleu_score['C4'].append(bleu_s)
                rouge_score['C4'].append(rouge_s)
                bleurt_score['C4'].append(bleurt_s)

        elif row['Task'][0] == 'M':
            if row['Task'][-1] == '2':
                bleu_score['M2'].append(bleu_s)
                rouge_score['M2'].append(rouge_s)
                bleurt_score['M2'].append(bleurt_s)
            elif row['Task'][-1] == '3':
                bleu_score['M3'].append(bleu_s)
                rouge_score['M3'].append(rouge_s)
                bleurt_score['M3'].append(bleurt_s)

    bleu_score_ls, rouge_score_ls, bleurt_score_ls, cider_score_ls, weighted_avg_ls = [], [], [], [], []

    for task in col[1:]:
        df = eval_csv[eval_csv['Task'] == task]
        cider_score_ls.append(
            compute_cider_score(list(df['gt']), list(df['pre_output'])) * 10)
        bleu_score_ls.append(
            sum(bleu_score[task]) / len(bleu_score[task]) * 100)
        rouge_score_ls.append(
            sum(rouge_score[task]) / len(rouge_score[task]) * 100)
        bleurt_score_ls.append(
            sum(bleurt_score[task]) / len(bleurt_score[task]) * 100)
        weighted_avg_ls.append(bleu_score_ls[-1] * 0.2 +
                               rouge_score_ls[-1] * 0.2 +
                               cider_score_ls[-1] * 0.2 +
                               bleurt_score_ls[-1] * 0.4)

    score_df = pd.DataFrame(columns=['Eval'] + col[1:])
    score_df.loc[len(score_df)] = ['BLEU-4'] + bleu_score_ls
    score_df.loc[len(score_df)] = ['ROUGE-L'] + rouge_score_ls
    score_df.loc[len(score_df)] = ['BLEURT'] + bleurt_score_ls
    score_df.loc[len(score_df)] = ['CIDEr'] + cider_score_ls
    score_df.loc[len(score_df)] = ['Weighted Avg'] + weighted_avg_ls
    score_df.to_csv(total_score_path, index=False)

    print('Classic Evaluation Finish! Score File was save in ' +
          total_score_path)


if __name__ == '__main__':
    sub_file = ''
    ref_path = ''
    save_path = ''


    score_file_path = os.path.join(save_path,'funqa_classic_score.csv')
    print('score_file_path: ', score_file_path)

    eval(sub_file, ref_path, score_file_path, 60)
