import numpy as np
number_dict={
    '1':'一',
    '2':'二',
    '3':'三',
    '4':'四'
}
def replaceNumber(n_str):
    number_list = [1,2,3,4,5,6,7,8]
    number_list = [str(number) for number in number_list]
    for number in number_list:
        if number in n_str:
            n_str = n_str.replace(number,number_dict[number])
    return  n_str

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

# 选择题
class ChoiceAnswer():
    def __init__(self, no,content):
        self.no = no
        self.content = str(content)
    def __str__(self):
        return "{}-{}".format(self.no,self.content)
# 填空题
class BlankAnswer():
    def __init__(self,no,content):
        self.no = no
        self.content = [cur_content for cur_content in content if cur_content != None]
        # print("content")
        # print(content)
        # print("self.content")
        # print(self.content)
# 解答题
class AnswerQuestion():
    def __init__(self,no,content):
        self.no = no
        self.content = [cur_content for cur_content in content if cur_content != None]
        # print("content")
        # print(content)
        # print("self.content")
        # print(self.content)
# 题目
class ProblemOjbect():
    def __init__(self,no,content):
        self.prob_no = no
        self.prob_content = content

    def __str__(self):
        return "{}-{}".format(self.prob_no,self.prob_content)
# 将一维列表转换为二维列表
def _1dTo2d_list(origin_list,dim):

    need_list = []
    temp_list = []
    for i,elem in enumerate(origin_list):
        # print(elem,type(elem))
        temp_list.append(elem)
        if (i+1) % dim == 0:
            need_list.append(temp_list)
            temp_list = []
    counter = 0
    for fuck in need_list:
        counter += len(fuck)
    # print(counter)
    # print(origin_list[counter:])
    need_list.append(origin_list[counter:])
    # for fuck in need_list:
    #     for cur_fuck in fuck:
    #         print(cur_fuck)
    return need_list

if __name__ == '__main__':
    str_o = '第1章'

    print(replaceNumber(str_o))
