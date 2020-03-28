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
if __name__ == '__main__':
    str_o = '第1章'

    print(replaceNumber(str_o))
