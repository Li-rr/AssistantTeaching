import os
import json
import sys
import re
import chardet
homeword_dir  = r"D:\WORKSPACE\助教工作\作业批改\作业数据"
work_name = ['第一章','第二章','第三章','第四章']

class Answer:
    def __init__(self,stuNo,stuName,workDate,workName):
        self.answernolist = []
        self.answerContentlist = []
        self.answerDict = {}
        self.answerDict['学号'] = stuNo
        self.answerDict['姓名'] = stuName
        self.answerDict['作业日期'] = workDate
        self.answerDict['作业名称'] = workName


    def add(self,answerNo,anserContent:list):

        # 如果是序号并且不在字典中
        if isFloat(answerNo) and answerNo not in self.answerDict.keys():
            self.answernolist.append(answerNo)  # 添加题目序号
            self.answerDict[answerNo] = anserContent
        elif isFloat(answerNo) and answerNo in self.answerDict.keys(): # 如果是序号并且在字典中
            self.answerDict[answerNo].append(anserContent)


        # 如果不可以当前序号不能转换为float，说明这个答案是多行答案
        if not isFloat(answerNo):
            print("++++",answerNo)
            t_answerno = self.answernolist[-1]  # 取最后一个
            self.answerDict[t_answerno].append(answerNo)
            print("---=-===-",t_answerno,self.answerDict[t_answerno])

# 判断字符串是否可以转换为浮点数
def isFloat(f_str):
    try:
        x = float(f_str)    # 此处更改想判断的类型
    except TypeError:
        return False
    except ValueError:
        return False
    except Exception as e:
        return False
    else:
        return True

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
            if i == 2:
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

        for file in submit_files:   # 遍历多个提交文件
            # print(file)
            submit_answer = {}  # 用于将答案转换为json

            file_split = re.split('[\\\,.]',file)
            print(file_split,len(file_split))

            stuNo = file_split[6].split('-')[0]
            stuName = file_split[6].split('-')[1]
            workDate = file_split[5]
            workName = file_split[7][-len(stuName):]
            print('作业日期 ({}) 学号 ({}) 姓名 ({}) 作业名称 {}'.format(workDate, stuNo, stuName, workName))
            assert workName in work_name, "作业名称错误"

            submit_answer['学号'] = stuNo
            submit_answer['姓名'] = stuName
            submit_answer['作业日期'] = workDate
            submit_answer['作业名称'] = workName
            # print(submit_answer)

            file_encoder = get_encoding(file)
            print(file_encoder)
            # 打开提交的文件
            with open(file,'r',encoding=file_encoder) as f:
                lines = f.readlines()
                lines = [line.strip() for line in lines]

            answer_dict = Answer(stuNo,stuName,workDate,workName)

            # 遍历当前文件中的所有行
            for i,line in enumerate(lines):
                print("=================》")
                # 首先需要把顿号替换为空格
                split_fuck_index = line.find('、') #查找顿号第一次出现的位置
                # print(line)

                if split_fuck_index != -1:  # 发现顿号
                    try:
                        # print('截取到的序号',line[:split_fuck_index])
                        answer_no = float(line[:split_fuck_index])
                        # line[split_fuck_index] = ' '
                        line = line.replace("、"," ",1)
                        # print(line[split_fuck_index])
                        # print(answer_no)
                    except: # 如果顿号不是分隔序号的
                        print("ERROR! 本行不含序号")
                        print(line)
                print("第{}行".format(i),line)
                answer_list = line.split()
                print(answer_list)
                if len(answer_list) == 0:
                    continue

                answer_no = answer_list[0]
                # if isFloat(answer_no):
                #     print("是答案序号")
                # else:
                #     print("不是答案序号")
                answer_content = answer_list[1:]
                answer_dict.add(answer_no,answer_content)
                print("答案序号：{}，答案内容：{}".format(answer_no,answer_content))

            json_str = json.dumps(answer_dict.answerDict,indent=2,ensure_ascii=False)
            file_name = '{}-{}-{}.json'.format(stuNo,stuName,workName)
            with open('workdata_dir/'+file_name,'w',encoding='utf-8') as json_file:
                json_file.write(json_str)
            # break


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

        file_encoder = get_encoding(file)
        print(file_encoder)

        # 打开文件
        with open(file,'r',encoding=file_encoder) as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]


        chapter_index_split = []
        chapter_name_list = []
        for line in lines:
            if line in work_name:   # 如果发现章节名称
                # 将章节答案的起始地址加入到列表中
                chapter_index_split.append(lines.index(line))
                chapter_name_list.append(line)

        split_index_1 = lines.index('第一章')
        split_index_2 = lines.index('第二章')
        all_chapter = []
        all_chapter.append(lines[split_index_1+1:split_index_2])
        all_chapter.append(lines[split_index_2+1:])
        for i,fuck_chapter in enumerate(all_chapter):
            submit_answer['作业名称'] = chapter_name_list[i]
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

            # print(submit_answer)
            json_str = json.dumps(submit_answer,indent=2,ensure_ascii=False)   # 缩进为2
            file_name = '{}-{}-{}.json'.format(stuNo,stuName,chapter_name_list[i])
            # print(file_name)
            with open('workdata_dir/'+file_name,'w',encoding='utf8') as json_file:
                json_file.write(json_str)
            # break
            # print(fuck_chapter)

# 获取文件编码类型
def get_encoding(file):
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        data = f.read()
        return chardet.detect(data)['encoding']


if __name__ == '__main__':
    dir_path = getHomeworkDir()
    getDataForCurrentData(dir_path)