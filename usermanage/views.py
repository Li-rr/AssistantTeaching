from django.shortcuts import render
from django.http import HttpResponse
from usermanage.models import Stu,Answer,Score,Problem
from usermanage.utils import replaceNumber,isFloat,ChoiceAnswer,BlankAnswer,AnswerQuestion
from usermanage.utils import _1dTo2d_list,ProblemOjbect,checkChoiceAnswer
from django.db.models import Q
import numpy as np
from django.core import serializers
import json
# Create your views here.

def index(request):
    return render(request,"index.html",{"title":"首页"})

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
    req_stuno = request.GET.get('stuno')

    print("请求数据 作业名称 {} 学号 {}".format(req_workname,req_stuno))
    if req_workname == None and req_stuno == None:
        req_workname = "第一章"
        req_stuno = "20161994"



    work_name_all = Score.objects.values('workname').distinct()
    work_name_list = []
    for work_name in work_name_all:
        work_name['workname'] = replaceNumber(work_name['workname'])
        if work_name['workname'] not in work_name_list:
            work_name_list.append(work_name['workname'])
    # print(work_name_list)
    stu_info = Score.objects.filter(workname=req_workname).values('stuno','stuname')   # 这里写死了，以后改
    answer_list = list(Score.objects.filter(workname = req_workname,stuno=req_stuno).values('worksubmit'))    # 这里写死了，以后改
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

    # 获取标准答案
    standard_answer_set = list(Answer.objects.filter(workname=req_workname).values("workanswer"))
    standard_answer_list = standard_answer_set[0]['workanswer']
    standard_answer_list = json.loads(standard_answer_list)
    # print(type(standard_answer_list),standard_answer_list)

    # -------- 取出学生的答案数据 -------------------
    blank_range,choice_range = 5,5
    # # print(answer_list)
    # print(standard_answer_list)
    # print(type(answer_list))
    for k,v in answer_list.items():
        # print(k,v,type(k),type(v))
        if isFloat(k):
            k_value = float(k)
            # print(k_value)
            if 1.0 <k_value < 2.0:   # 选择题
                try:
                    v_f = v[0]
                except:
                    v_f = 'e'

                choice_answer.append(ChoiceAnswer(k,v_f))
            elif 2.0 < k_value <3.0:    # 填空题
                blanks_answer.append(BlankAnswer(k,v))  # 添加序号和内容，分别为字符串和列表
            else:   # 解答题
                answer_questions.append(AnswerQuestion(k,v))

    choice_answer_bak = choice_answer

    choice_answer = _1dTo2d_list(choice_answer,choice_range)
    blanks_answer = _1dTo2d_list(blanks_answer,blank_range)

    # --------------- 检查选择题答案，返回错误选择题的答案序号
    wrongChoice_list = checkChoiceAnswer(standard_answer_list,choice_answer_bak)
    # wrongChoice_list += ['1.2','1.3','1.4']
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
                      'problem_answer_list':prob_answer_list,
                      'req_workname':req_workname,
                      'req_stuno':req_stuno,
                      'wrong_choice_list':wrongChoice_list,
                      "title":"作业管理"
                  })

# 存储提交上来的错题序号
def storeWrongProblem(request):
    stuno = request.GET.get("stuno");
    workname = request.GET.get("workname");
    wrong_choice = request.GET.get("choice");
    wrong_blank = request.GET.get("blank");
    wrong_quest_answer = request.GET.get("quest_answer");


    wrongall = []
    wrongall ="有问题的题目：{} {} {}".format(wrong_choice , wrong_blank , wrong_quest_answer)
    print("{} {} {} {} {}".format(stuno,workname,wrong_choice,wrong_blank,wrong_quest_answer))
    print(wrongall)

    # f_str = {"stuno":stuno,"workname":workname}
    Score.objects.filter(Q(stuno=stuno)&Q(workname=workname)).update(workcorrection=wrongall )

    return  HttpResponse("success")

def homeResult(request):
    # --- 获取请求数据
    req_workname = request.GET.get('workname')
    req_stuno = request.GET.get('stuno')
    print("请求数据 作业名称 {} 学号 {}".format(req_workname,req_stuno))
    if req_workname == None and req_stuno == None:
        req_workname = "第一章"
        req_stuno = "20161994"

    # -------获取作业名称
    work_name_all = Score.objects.values('workname').distinct()
    work_name_list = []
    for work_name in work_name_all:
        work_name['workname'] = replaceNumber(work_name['workname'])
        if work_name['workname'] not in work_name_list:
            work_name_list.append(work_name['workname'])

    # ------获取学生信息
    stu_info = Score.objects.filter(workname=req_workname).values('stuno','stuname','workcorrection','workname')
    # print(stu_info)
    # answer_list = list(Score.objects.filter(workname = req_workname,stuno=req_stuno).values('worksubmit'))
    # answer_list = answer_list[0]['worksubmit']
    # answer_list = json.loads(answer_list)
    return render(request,"h_homeresult.html",
                  {
                      "title":"作业结果",
                      "workname_list":work_name_list,
                      "stu_info":stu_info,
                      'req_workname': req_workname,
                      'req_stuno': req_stuno
                  })
def test(request):
    return render(request,'h_workManage.html',{'test':"这里是测试"})

