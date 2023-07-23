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


def calculate_bleu4(reference, hypothesis):
    # 将字符串分词为列表
    ref_tokens = reference.split()
    hyp_tokens = hypothesis.split()
    blue4_score = sentence_bleu([ref_tokens], hyp_tokens, weights=(0.25, 0.25, 0.25, 0.25), smoothing_function=SmoothingFunction().method1)

    return blue4_score
def calculate_rouge(reference, hypothesis):
    rouge = Rouge()
    rouge_score = rouge.get_scores(hypothesis, reference, avg=True)
    return rouge_score['rouge-l']['f']


def compute_cider_score(reference, candidate):
    gts = {}
    res = {}
    for idx in range(len(reference)):
        gts[idx]=[reference[idx]]
        res[idx]=[candidate[idx]]

    # 初始化CIDEr评估器
    cider_scorer = Cider()

    # 计算CIDEr分数
    cider_score, _ = cider_scorer.compute_score(gts, res)
    return cider_score

openai.api_key ='' # 改为自己的
def extract_last_integer(string):
    # 使用正则表达式匹配最后一个整数
    match = re.search(r'\d+$', string)

    if match:
        last_integer = int(match.group())
        return last_integer
    else:
        # 如果字符串中没有整数，则返回None或其他默认值
        print('No integers in this string.')
        return 0

def get_score(output,ground_truth,task):

    system_messages = {
        'des':'''
        You will be given two text segments in the following format: [text1][text2]. These two texts will be descriptions of a counterintuitive (humorous, creative, or magical) video. For text2, your task is to provide a score based on the following criteria:
        1. Content: Score out of 20 points. If the content is nearly identical, award 20 points. If the content differs slightly, deduct 5 points. If the content differs significantly, deduct 10 points. If the content differs greatly, deduct 15 points. If the content is completely different, deduct 20 points.
        2. Details: Score out of 50 points. Describe the video's details, including characters, scenes, actions, dialogues, etc. Deduct 5 points for each differing detail. Clearly identify and count the differing details to calculate the final score.
        3. Logic: Score out of 20 points. The description should be logically consistent without any unreasonable situations. If the logic is nearly identical, award 20 points. If the logic is generally consistent but differs in details, award 15 points. If there are some differences in logic but still similar overall, award 10 points. If there are significant differences in logic, award 5 points.
        4. Language Expression: Score out of 10 points. Evaluate the fluency and word usage of the text. If the language expression is at a consistent level, award 10 points. If there are minor differences in language expression, award 5 points. If there are significant differences in language expression, award 0 points.
        Note: If the content differs significantly, multiply the total score by 0.5. If the content differs greatly, multiply the total score by 0.25.
        ''',
        'exp':'''
        You will be given two text segments in the following format: [text1][text2]. These two texts will be explanations for a counterintuitive video (humorous, creative, or magical). For text2, your task is to provide a score based on the following criteria:
        1. Language Expression: Score out of 5 points. Evaluate the fluency and word usage of the text. If the language expression is at a consistent level, award 5 points. If there are significant differences in language expression, award 0 points.
        2. Logic: Score out of 10 points. The explanation should be logically sound, preferably with logical words and cause-effect relationships. If the logic is nearly identical, award 10 points. If the logic is generally consistent but differs in details, award 5 points. If there are some differences in logic but still similar overall, award 5 points. If there are significant differences in logic, award 0 points.
        3. Common Sense Errors: Score out of 10 points. The explanation should not contain any obvious common sense errors. Deduct 5 points for each occurrence of a common sense error.
        4. Understanding of Humor, Creativity, or Magic: Score out of 40 points. If the explanation focuses on the same key points as the reference answer, award 35 points or above. If the explanation provides reasons for the counterintuitive phenomenon but differs from the reference answer, award between 15-35 points based on the difference. If the explanation provides reasons for the counterintuitive phenomenon but differs greatly from the reference answer, award between 0-15 points.
        5. Details: Score out of 35 points. While providing the explanation, include video details that contribute to the humor, creativity, or magical effect. Deduct 5 points for each additional or missing detail compared to the reference answer.
        6. If the explanation differs significantly from the reference answer and includes descriptive details not mentioned in the reference answer, multiply the total score by 0.5.
        7. The minimum score is 0, and the maximum score is 100.
        ''',
        'title':'''
        You will be given four text segments in the following format: [Description][Explanation][text1][text2]. The first two texts are descriptions of a video and its explanation, respectively. The third text is a reference title. Your task is to evaluate whether the fourth text is a good title. Note that the fourth text may not be a title but a statement including the video. In that case, extract the actual title and evaluate it. Consider the following points while assigning a score:
        1. The title should mention the content of the video.
        2. A title with a certain level of humor or creativity is preferable.
        Provide a score ranging from 0 to 100, considering the above criteria.
        ''',
    }
    task_mapping = ['','','des','exp','title']
    gpt_input = '[' + ground_truth + '] [' + output +']'
    for _ in range(3):
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[{
                    'role': 'system',
                    'content': system_messages[task_mapping[int(task[-1])]],
                }, {
                    'role': 'user',
                    'content': gpt_input,
                }],
                temperature=0.7,
                max_tokens=1024,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None,
            )
            ans = response['choices'][0]['message']['content']
            score = extract_last_integer(ans)
            return score
        except Exception as e:
            print('[ERROR]', e)
            ans =  '#ERROR#'
            time.sleep(1)
    return score

def eval_gpt(submission_json,ground_truth_json):
    scores = {
        'H2':0,
        'H3':0,
        'H4':0,
        'C2':0,
        'C3':0,
        'C4':0,
        'M2':0,
        'M3':0,
    }
    cnt = {
        'H2':0,
        'H3':0,
        'H4':0,
        'C2':0,
        'C3':0,
        'C4':0,
        'M2':0,
        'M3':0,
    }
    with open(submission_json) as f:
        submission = json.load(f)
    with open(ground_truth_json) as f:
        ground_truth = json.load(f)
    for i,j in zip(submission,ground_truth):
        this_score = get_score(i['output'],j['output'],i['task'])
        scores[i['task']] += this_score
        cnt[i['task']] += 1
    for i in scores:
        scores[i] /= cnt[i]
    return scores

def eval(submission_file, answer_file, total_score_path, run_time):
    print('Validating...')
    col = ['Task', 'H2', 'H3', 'H4', 'C2', 'C3', 'C4', 'M2', 'M3']
    with open(submission_file) as f:
        submission = json.load(f)
    with open(answer_file) as f:
        answer = json.load(f)

    chk_answer = []
    for data in answer:
        chk_answer.append(
            {'task': data['task'], 'output': data['output'], "instruction": data['instruction'], "ID": data['ID']})

    diff = False
    for data in submission:
        if {'task': data['task'], 'output': data['output'], "instruction": data['instruction'], "ID": data['ID']} not in chk_answer:
            diff = True
            break

    assert diff == False, "Submission file is not valid"
    print('File is valid! Loading File...')

    submission = sorted(submission, key=lambda x: x['ID'])
    answer = sorted(answer, key=lambda x: x['ID'])

    can_path = 'bleurt/test_data/candidates'
    ref_path = 'bleurt/test_data/references'
    with open(can_path, 'w') as f_can:
        f_can.close()
    with open(ref_path, 'w') as f_ref:
        f_ref.close()

    bleurt_score_path = 'score.txt'
    eval_csv = pd.DataFrame(columns=['pre_output', 'gt', 'Task', 'bleurt_score'])
    for i in tqdm(range(len(submission))):
        pre_output = submission[i]['output']
        gt = answer[i]['output']

        with open(can_path, 'a') as f_can:
            f_can.write(pre_output + '\n')
        with open(ref_path, 'a') as f_ref:
            f_ref.write(gt + '\n')
        task = answer[i]['task']
        eval_csv = pd.concat([eval_csv, pd.DataFrame([[pre_output, gt, task, 0]], columns=['pre_output', 'gt', 'Task', 'bleurt_score'])])

    f_can.close()
    f_ref.close()

    os.system('python -m bleurt.score_files   -candidate_file={}  -reference_file={}   -bleurt_checkpoint=BLEURT-20   -scores_file={}'
              .format(can_path, ref_path, bleurt_score_path))

    from time import sleep
    sleep(run_time)

    with open(bleurt_score_path) as f:
        eval_csv['bleurt_score'] = [i[:-1] for i in f.readlines()]

    rouge_score, bleu_score, bleurt_score, cider_score = {}, {}, {}, {}
    gpt_score = eval_gpt(submission_file, answer_file)
    bleurt_score['H2'], bleurt_score['H3'], bleurt_score['H4'], bleurt_score['C2'], bleurt_score['C3'], bleurt_score['C4'], bleurt_score['M2'], bleurt_score['M3'] = [], [], [], [], [], [], [], []
    rouge_score['H2'], rouge_score['H3'], rouge_score['H4'], rouge_score['C2'], rouge_score['C3'], rouge_score['C4'], rouge_score['M2'], rouge_score['M3'] = [], [], [], [], [], [], [], []
    bleu_score['H2'], bleu_score['H3'], bleu_score['H4'], bleu_score['C2'], bleu_score['C3'], bleu_score['C4'], bleu_score['M2'], bleu_score['M3'] = [], [], [], [], [], [], [], []

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

    bleu_score_ls, rouge_score_ls, bleurt_score_ls, cider_score_ls, gpt_score_ls, weighted_avg_ls = [], [], [], [], [], []
    for task in col[1:]:
        df = eval_csv[eval_csv['Task'] == task]
        cider_score_ls.append(compute_cider_score(list(df['gt']), list(df['pre_output'])) * 10)
        bleu_score_ls.append(sum(bleu_score[task])/len(bleu_score[task]) * 100)
        rouge_score_ls.append(sum(rouge_score[task])/len(rouge_score[task]) * 100)
        bleurt_score_ls.append(sum(bleurt_score[task])/len(bleurt_score[task]) * 100)
        gpt_score_ls.append(gpt_score[task])
        weighted_avg_ls.append(bleu_score_ls[-1] * 0.1 + rouge_score_ls[-1] * 0.1 + cider_score_ls[-1] * 0.1 + bleurt_score_ls[-1] * 0.2 + gpt_score_ls[-1] * 0.5)
    
    
    score_df = pd.DataFrame(columns=['Eval'] + col[1:])
    score_df.loc[len(score_df)] = ['BLEU-4'] + bleu_score_ls
    score_df.loc[len(score_df)] = ['ROUGE-L'] + rouge_score_ls
    score_df.loc[len(score_df)] = ['BLEURT'] + bleurt_score_ls
    score_df.loc[len(score_df)] = ['CIDEr'] + cider_score_ls
    score_df.loc[len(score_df)] = ['GPT-4'] + gpt_score_ls
    score_df.loc[len(score_df)] = ['Weighted Avg'] + weighted_avg_ls
    score_df.loc[len(score_df)] = ['Final Score'] + [list(score_df['H2'])[-1] * 0.15 + list(score_df['H3'])[-1] * 0.15 + list(score_df['H4'])[-1] * 0.05 + list(score_df['C2'])[-1] * 0.15 + list(score_df['C3'])[-1] * 0.15 + list(score_df['C4'])[-1] * 0.05 + list(score_df['M2'])[-1] * 0.15 + list(score_df['M3'])[-1] * 0.15] + [''] * 7
    score_df.to_csv(total_score_path, index=False)

    print('Finish! Score File was save in ' + total_score_path)

if __name__ == '__main__':
    eval("subbmision.json", "funqa_test.json", "total_score.csv", 60)