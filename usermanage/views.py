from django.shortcuts import render
from django.http import HttpResponse
from usermanage.models import Stu,Answer,Score,Problem
from usermanage.utils import replaceNumber,isFloat,ChoiceAnswer,BlankAnswer,AnswerQuestion
from usermanage.utils import _1dTo2d_list,ProblemOjbect
import numpy as np
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
    #--- 获取请求数据

    req_workname = request.GET.get('workname')
    print("请求数据 {}".format(req_workname))
    if req_workname == None:
        req_workname = "第一章"



    work_name_all = Score.objects.values('workname').distinct()
    work_name_list = []
    for work_name in work_name_all:
        work_name['workname'] = replaceNumber(work_name['workname'])
        if work_name['workname'] not in work_name_list:
            work_name_list.append(work_name['workname'])
    # print(work_name_list)
    stu_info = Score.objects.filter(workname=req_workname).values('stuno','stuname')   # 这里写死了，以后改
    answer_list = list(Score.objects.filter(workname = req_workname,stuno='20161994').values('worksubmit'))    # 这里写死了，以后改
    answer_list = answer_list[0]['worksubmit']
    answer_list = json.loads(answer_list)

    # 获取填空题&解答题数据
    problem_list = list(Problem.objects.filter(workname=req_workname).values("wrokcontent"))   # 这里写死了，以后改
    problem_list = problem_list[0]['wrokcontent']
    problem_list = json.loads(problem_list)
    # print(problem_list)
    choice_answer = []  # 选择题
    blanks_answer = []  # 填空题
    answer_questions = [] # 解答题


    # -------- 取出学生的答案数据 -------------------
    blank_range,choice_range = 5,5
    # print(answer_list)
    # print(type(answer_list))
    for k,v in answer_list.items():
        # print(k,v,type(k),type(v))
        if isFloat(k):
            k_value = float(k)
            # print(k_value)
            if 1.0 <k_value < 2.0:   # 选择题
                choice_answer.append(ChoiceAnswer(k,v[0]))
            elif 2.0 < k_value <3.0:    # 填空题
                blanks_answer.append(BlankAnswer(k,v))  # 添加序号和内容，分别为字符串和列表
            else:   # 解答题
                answer_questions.append(AnswerQuestion(k,v))

    choice_answer = _1dTo2d_list(choice_answer,choice_range)
    blanks_answer = _1dTo2d_list(blanks_answer,blank_range)

    # --------------- 取出填空题&解答题数据
    prob_answer_list = []
    for k,v in problem_list.items():
        prob_answer_list.append((ProblemOjbect(k,v)))

    # print(stu_info)
    return render(request,'h_workManage.html',
                  {
                      "workname_list":work_name_list,
                      "stu_info":stu_info,
                      'choice_double_answer_list':choice_answer,
                      'blanks_double_answer_list':blanks_answer,
                      'answer_question_list':answer_questions,
                      'problem_answer_list':prob_answer_list
                  })

def test(request):
    return render(request,'h_workManage.html',{'test':"这里是测试"})

