import os
import json
import sys
import re
homeword_dir  = r"D:\WORKSPACE\助教工作\作业批改\作业数据"
work_name = ['第一章','第二章','第三章','第四章']

def getHomeworkDir():
    dir_list = []   # 存储收集到的作业集合
    for cur_dir in os.listdir(homeword_dir):
        dir_path = os.path.join(homeword_dir, cur_dir)
        if os.path.isdir(dir_path):
            dir_list.append(dir_path)

    return dir_list

# 分析当前日期收集的作业
def getDataForCurrentData(dir_list):
    stu_work_dirs = []
    for dir in dir_list:
        # print(os.listdir(dir))
        stu_work_dirs = [os.path.join(dir,t_dir) for t_dir in os.listdir(dir) if os.path.isdir(os.path.join(dir,t_dir))]  # 获得包括学生提交的作业附件
        # print(type(stu_work_dirs),len(stu_work_dirs))
        for i,stu_dir in enumerate(stu_work_dirs):
            # print(stu_dir)
            if i == 1:
                break
            print("\n===========>")
            getStuentWorkDir_data(stu_dir)



# 获取学生提交文件夹内的附件
def getStuentWorkDir_data(dir_path):
    files = os.listdir(dir_path)
    submit_files = [os.path.join(dir_path,t_file) for t_file in files]
    print(submit_files,len(submit_files))
    # 先处理提交两个文件的情况
    if len(submit_files) == 2:
        for file in submit_files:
            # print(file)
            file_split = re.split('[\\\,.]',file)
            print(file_split,len(file_split))

            stuNo = file_split[6].split('-')[0]
            stuName = file_split[6].split('-')[1]
            workDate = file_split[5]
            workName = file_split[7][-len(stuName):]
            print('作业日期 ({}) 学号 ({}) 姓名 ({}) 作业名称 {}'.format(workDate, stuNo, stuName, workName))
            assert workName in work_name, "作业名称错误"



    elif len(submit_files) == 1:
        submit_answer = {}      # 用于读取上的答案转换为json

        file = submit_files[0]

        file_split = re.split('[\\\,.]',file)
        print(file_split,len(file_split))
        stuNo = file_split[6].split('-')[0]
        stuName = file_split[6].split('-')[1]
        workDate = file_split[5]
        # workName = file_split[8][-len(stuName):]

        submit_answer['学号'] = stuNo
        submit_answer['姓名'] = stuName
        submit_answer['作业日期'] = workDate
        print('作业日期 ({}) 学号 ({}) 姓名 ({})'.format(workDate, stuNo, stuName))

        # 打开文件
        with open(file,'r',encoding='utf8') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]


        chapter_index_split = []
        chapter_name_list = []
        for line in lines:
            if line in work_name:   # 如果发现章节名称
                print(lines.index(line))
                # 将章节答案的起始地址加入到列表中
                chapter_index_split.append(lines.index(line))
                chapter_name_list.append(line)

        split_index_1 = lines.index('第一章')
        split_index_2 = lines.index('第二章')
        all_chapter = []
        all_chapter.append(lines[split_index_1+1:split_index_2])
        all_chapter.append(lines[split_index_2+1:])
        for fuck_chapter in all_chapter:
            for answer in fuck_chapter:
                answer_split = answer.split(" ")
                answer_no = answer_split[0]
                answer_content_list = answer_split[1:]
                try:
                    float(answer_split[0])
                except:
                    print("答案序号必须是数字")

                submit_answer[answer_no]= answer_content_list
                # print("答案序号 {},  答案内容 {}".format(answer_no,answer_content_list))
                # print(answer_split)

            break
            print(fuck_chapter)
        # print(submit_answer)


if __name__ == '__main__':
    dir_path = getHomeworkDir()
    getDataForCurrentData(dir_path)