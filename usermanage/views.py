from django.shortcuts import render
from django.http import HttpResponse
from usermanage.models import Stu
# Create your views here.

def index(request):
    return render(request,"index.html")

def getStuTable(request):
    all_stu = Stu.objects.all()
    print(type(all_stu),len(all_stu))
    print(all_stu[0],type(all_stu[0]))
    return render(request,'stuTable.html',{'all_stu':all_stu})

