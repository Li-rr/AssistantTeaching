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
        self.no = float(no)
        self.content = str(content)
    def __str__(self):
        return "{}-{}".format(self.no,self.content)
# 填空题
class BlankAnswer():
    def __init__(self,no,content):
        self.no = float(no)
        self.content = content
# 解答题
class AnswerQuestion():
    def __int__(self,no,content):
        self.no = float(no)
        self.content = content

if __name__ == '__main__':
    str_o = '第1章'

    print(replaceNumber(str_o))
