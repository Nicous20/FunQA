import json
json_file_path = '/home/bli/FunQA/data/0000/submission/submission.json'
with open(json_file_path) as f:
    data = json.load(f)

video_ls = []
H_ls = []
C_ls = []
M_ls = []

# 取出data中每一个item的instrction，不要重复：
for item in data:
    if item['visual_input'] not in video_ls:
        video_ls.append(item['visual_input'])
        if item['visual_input'][0] == 'H':
            H_ls.append(item['visual_input'])
        elif item['visual_input'][0] == 'C':
            C_ls.append(item['visual_input'])
        else:
            M_ls.append(item['visual_input'])

sample_H_ls = []
sample_C_ls = []
sample_M_ls = []
import random
random.shuffle(H_ls)
sample_H_ls = H_ls[:int(len(H_ls) * 0.25)]

random.shuffle(C_ls)
sample_C_ls = C_ls[:int(len(C_ls) * 0.25)]

random.shuffle(M_ls)
sample_M_ls = M_ls[:int(len(M_ls) * 0.25)]

sample_video_ls = sample_H_ls + sample_C_ls + sample_M_ls


# save sample_video_ls as json file
with open('sample_video_ls_0000.json', 'w') as f:
    json.dump(sample_video_ls, f)