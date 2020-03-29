from django.shortcuts import render
from django.http import HttpResponse
from usermanage.models import Stu,Answer,Score
from usermanage.utils import replaceNumber,isFloat,ChoiceAnswer
from django.core import serializers
import json
# Create your views here.

def index(request):
    return render(request,"index.html")

# 返回学生名单
def getStuTable(request):
    all_stu = Stu.objects.all()
    print(type(all_stu),len(all_stu))
    print(all_stu[0],type(all_stu[0]))
    return render(request,'stuTable.html',{'all_stu':all_stu})

# 考勤管理
def attendanceManage(request):
    return HttpResponse("这里是考勤管理")

# 作业管理
def homeworkManage(request):
    work_name_all = Score.objects.values('workname').distinct()
    work_name_list = []
    for work_name in work_name_all:
        work_name['workname'] = replaceNumber(work_name['workname'])
        if work_name['workname'] not in work_name_list:
            work_name_list.append(work_name['workname'])
    # print(work_name_list)
    stu_info = Score.objects.filter(workname='第一章').values('stuno','stuname')
    answer_list = list(Score.objects.filter(workname = "第一章",stuno='20161994').values('worksubmit'))
    answer_list = answer_list[0]['worksubmit']
    answer_list = json.loads(answer_list)
    choice_answer = []  # 选择题
    blanks_answer = []  # 填空题
    answer_questions = [] # j解答题
    temp_list = []
    choice_counter = 1
    choice_range = 5
    # print(answer_list)
    # print(type(answer_list))
    for k,v in answer_list.items():
        # print(k,v,type(k),type(v))
        if isFloat(k):
            k_value = float(k)
            # print(k_value)
            if 1.0 <k_value < 2.0:   # 选择题
                temp_list.append(ChoiceAnswer(k,v[0]))
                if choice_counter%choice_range == 0:
                    print('choice_counter',choice_counter)
                    choice_answer.append(temp_list)
                    temp_list= []
                choice_counter += 1
            elif 2.0 < k_value <3.0:    # 填空题
                blanks_answer.append((k,v))
            else:   # 解答题
                answer_questions.append((k,v))


    # print(answer_list[0]['worksubmit'])

    print(choice_answer)
    # print()
    # print(blanks_answer)
    # print()
    # print(answer_questions)

    # print(stu_info)
    return render(request,'h_workManage.html',
                  {
                      "workname_list":work_name_list,
                      "stu_info":stu_info,
                      'choice_double_answer_list':choice_answer,
                      'blanks_answer_list':blanks_answer,
                      'answer_question_list':answer_questions
                  })



