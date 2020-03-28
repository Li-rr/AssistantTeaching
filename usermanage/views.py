from django.shortcuts import render
from django.http import HttpResponse
from usermanage.models import Stu,Answer,Score
from usermanage.utils import replaceNumber
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
    return render(request,'h_workManage.html',{"workname_list":work_name_list})



