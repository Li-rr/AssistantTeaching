from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('stuTable/', views.getStuTable, name="getTable"),
    path('attn/', views.attendanceManage, name="attnManage"),
    path('homework/', views.homeworkManage, name="homeworkManage"),
    path("storewrong/",views.storeWrongProblem,name="storewrong"),
    path("homeresult/",views.homeResult,name="homeResult"),
    path('test/', views.test, name="test"),
]
