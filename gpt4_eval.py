import pandas as pd
from tqdm import tqdm
import os
import time
import openai
import json
import re
import sys


def extract_last_number(string):

    # Use regular expression to match last number
    match = re.search(r'\d+(\.\d*)?(?=[^\d.]*$)', string)

    if match:
        last_integer = float(match.group())
        return last_integer
    else:
        # If there is no integer in the string, return None or other default value
        print('No integers in this string.')
        return 0


def get_score(cache_ls, output, ground_truth, task):
    max_len = {
        'H2': 150,
        'H3': 180,
        'H4': 40,
        'C2': 390,
        'C3': 310,
        'C4': 30,
        'M2': 180,
        'M3': 130
    }
    if output == '':
        return '', 0
    if len(output) > max_len[task]:
        output = output[:max_len[task]]
    system_messages = {
        'des':
        '''
        You will be given two text segments in the following format: [text1][text2]. These two texts will be descriptions of a counterintuitive (humorous, creative, or magical) video. For text2, your task is to provide a score based on the following criteria:
        1. Content: Score out of 20 points. If the content is nearly identical, award 20 points. If the content differs slightly, deduct 5 points. If the content differs significantly, deduct 10 points. If the content differs greatly, deduct 15 points. If the content is completely different, deduct 20 points.
        2. Details: Score out of 50 points. Describe the video's details, including characters, scenes, actions, dialogues, etc. Deduct 5 points for each differing detail. Clearly identify and count the differing details to calculate the final score.
        3. Logic: Score out of 20 points. The description should be logically consistent without any unreasonable situations. If the logic is nearly identical, award 20 points. If the logic is generally consistent but differs in details, award 15 points. If there are some differences in logic but still similar overall, award 10 points. If there are significant differences in logic, award 5 points.
        4. Language Expression: Score out of 10 points. Evaluate the fluency and word usage of the text. If the language expression is at a consistent level, award 10 points. If there are minor differences in language expression, award 5 points. If there are significant differences in language expression, award 0 points.
        Note: If the content differs significantly, multiply the total score by 0.5. If the content differs greatly, multiply the total score by 0.25.
        The output format is (remember not to have any comments, directly output scores) :
        [Content: Score], [Details: Score], [Logic: Score], [Language: Score], [Factor: 1 or 0.5 or 0.25]
        [Final Score]
        ''',
        'exp':
        '''
        You will be given two text segments in the following format: [text1][text2]. These two texts will be explanations for a counterintuitive video (humorous, creative, or magical). For text2, your task is to provide a score based on the following criteria:
        1. Language Expression: Score out of 5 points. Evaluate the fluency and word usage of the text. If the language expression is at a consistent level, award 5 points. If there are significant differences in language expression, award 0 points.
        2. Logic: Score out of 10 points. The explanation should be logically sound, preferably with logical words and cause-effect relationships. If the logic is nearly identical, award 10 points. If the logic is generally consistent but differs in details, award 5 points. If there are some differences in logic but still similar overall, award 5 points. If there are significant differences in logic, award 0 points.
        3. Common Sense Errors: Score out of 10 points. The explanation should not contain any obvious common sense errors. Deduct 5 points for each occurrence of a common sense error.
        4. Understanding of Humor, Creativity, or Magic: Score out of 40 points. If the explanation focuses on the same key points as the reference answer, award 35 points or above. If the explanation provides reasons for the counterintuitive phenomenon but differs from the reference answer, award between 15-35 points based on the difference. If the explanation provides reasons for the counterintuitive phenomenon but differs greatly from the reference answer, award between 0-15 points.
        5. Details: Score out of 35 points. While providing the explanation, include video details that contribute to the humor, creativity, or magical effect. Deduct 5 points for each additional or missing detail compared to the reference answer.
        6. If the explanation differs significantly from the reference answer and includes descriptive details not mentioned in the reference answer, multiply the total score by 0.5.
        7. The minimum score is 0, and the maximum score is 100.
        The output format is (remember not to have any comments, directly output scores) :
        [Language: Score], [Logic: Score], [Common Sense Errors: Score], [Understanding: Score], [Details: Score], [Factor: 1 or 0.5 or 0.25]
        [Final Score]
        ''',
        'title':
        '''
        You will be given four text segments in the following format: [Description][Explanation][text1][text2]. The first two texts are descriptions of a video and its explanation, respectively. The third text is a reference title. Your task is to evaluate whether the fourth text is a good title. Note that the fourth text may not be a title but a statement including the video. In that case, extract the actual title and evaluate it. Consider the following points while assigning a score:
        1. The title should mention the content of the video.
        2. A title with a certain level of humor or creativity is preferable.
        Provide a score ranging from 0 to 100, considering the above criteria and tell the reason.
        The output format is:
        [Final Score]
        ('Final Score' are in square bracketsremember! Just one line! Remember not to have any comments, directly output scores. Remember DO NOT GIVE ME EXPLANATION!!!!!!!!!) :
        ''',
    }
    task_mapping = ['', '', 'des', 'exp', 'title']
    gpt_input = '[' + ground_truth + '] [' + output + ']'
    if task[-1] == '4':
        gpt_input = '[' + cache_ls[0] + '] [' + cache_ls[
            1] + ']' + '[' + ground_truth + '] [' + output + ']'
    for _ in range(3):
        time.sleep(5)
        try:
            response = openai.ChatCompletion.create(
                model='gpt-4',
                messages=[{
                    'role':
                    'system',
                    'content':
                    system_messages[task_mapping[int(task[-1])]],
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
            score = extract_last_number(ans)
            return ans, score
        except Exception as e:
            print('[ERROR]', e)
            ans = '#ERROR#'
            time.sleep(5)
            return ans, 0


def eval(submission_file, ground_file, sample_id_path, total_score_path,
         json_output_path, openai_key):
    print('Validating...')
    col = ['Task', 'H2', 'H3', 'H4', 'C2', 'C3', 'C4', 'M2', 'M3']
    with open(submission_file) as f:
        submission = json.load(f)
    with open(ground_file) as f:
        gt = json.load(f)

    chk_answer = []
    for data in gt:
        chk_answer.append({
            'task': data['task'],
            'instruction': data['instruction'],
            'ID': data['ID']
        })

    diff = False
    for data in submission:
        if {
                'task': data['task'],
                'instruction': data['instruction'],
                'ID': data['ID']
        } not in chk_answer:
            print({
                'task': data['task'],
                'instruction': data['instruction'],
                'ID': data['ID']
            })
            diff = True
            break

    assert diff is False, 'Submission file is not valid'
    print('File is valid! \n Loading File...')

    openai.api_key = openai_key  # 改为自己的

    submission = sorted(submission, key=lambda x: int(x['ID'].split('_')[-1]))
    gt = sorted(gt, key=lambda x: int(x['ID'].split('_')[-1]))

    gpt_score = {
        'H2': 0,
        'H3': 0,
        'H4': 0,
        'C2': 0,
        'C3': 0,
        'C4': 0,
        'M2': 0,
        'M3': 0,
    }
    cnt = {
        'H2': 0,
        'H3': 0,
        'H4': 0,
        'C2': 0,
        'C3': 0,
        'C4': 0,
        'M2': 0,
        'M3': 0,
    }

    output_ls = []

    print('Start GPT-4 Evaluating...')

    cache_ls = []

    with open(sample_id_path) as f:
        sample_video_ls = json.load(f)

    counter = 1
    for i, j in tqdm(list(zip(submission, gt))):
        counter += 1
        if counter % (len(submission) // 10) == 0:
            with open(
                    json_output_path.split('.')[0] + '_' +
                    str(counter * 10 // len(submission)) + '.json', 'w') as f:
                json.dump(output_ls, f)

        if j['visual_input'] not in sample_video_ls:
            continue

        count = 0
        gpt_res, score = get_score(cache_ls, i['output'], j['output'],
                                   i['task'])
        while score == 0 and count < 3:
            count += 1
            gpt_res, score = get_score(cache_ls, i['output'], j['output'],
                                       i['task'])

        output_ls.append({
            'instruction': i['instruction'],
            'visual_input': i['visual_input'],
            'output': i['output'],
            'task': i['task'],
            'ID': i['ID'],
            'GPT-4-res': gpt_res,
            'GPT-4-score': score
        })

        # saving:

        gpt_score[i['task']] += score
        cnt[i['task']] += 1

        if j['task'][0] != 'M':
            if j['task'][-1] != '4':
                cache_ls.append(j['output'])
            else:
                cache_ls = []

    for i in gpt_score:
        if cnt[i] == 0:
            continue
        gpt_score[i] /= cnt[i]

    with open(json_output_path, 'w') as f:
        json.dump(output_ls, f)

    gpt_score_ls = []
    for task in col[1:]:
        gpt_score_ls.append('{:.2f}'.format(gpt_score[task]))

    score_df = pd.DataFrame(columns=['Eval'] + col[1:])

    score_df.loc[len(score_df)] = ['GPT-4'] + gpt_score_ls

    score_df.to_csv(total_score_path, index=False)

    print('GPT-4 Evaluation Finish! \nScore File was save in ' +
          total_score_path + '\nGPT Response File was save in ' +
          json_output_path)


if __name__ == '__main__':
    # Read command line arguments
    sub_file = sys.argv[1]
    ref_path = sys.argv[2]
    sample_id_path = sys.argv[3]
    save_path = sys.argv[4]
    output_path = sys.argv[5]
    date = sys.argv[6]
    openai_key = sys.argv[7]

    team_id = os.path.basename(sub_file).split('.json')[0]
    grade_path = os.path.join(save_path, team_id)
    output_path_team = os.path.join(output_path, team_id)
    if not os.path.exists(grade_path):
        os.makedirs(grade_path)
    if not os.path.exists(output_path_team):
        os.makedirs(output_path_team)

    score_file_path = os.path.join(grade_path,
                                   team_id + '_gpt_score_' + date + '.csv')
    output_json_path = os.path.join(output_path_team,
                                    team_id + '_json_' + date + '.json')
    print(score_file_path, output_json_path)

    eval(sub_file, ref_path, sample_id_path, score_file_path, output_json_path,
         openai_key)
