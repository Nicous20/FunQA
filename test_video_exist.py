import os
import json

ann = []
f='data/creative/creative_new.json'
ann += json.load(open(f, 'r'))

#file_names = ['file1.txt', 'file2.txt', 'file3.txt']
video_id=[]
for item in ann:
    video_id.append(item['visual_input'])

path = 'video_root/'

# 检查文件是否存在并输出不存在的文件名
for file_name in video_id:
    if not os.path.exists(os.path.join(path, file_name)):
        print(file_name)