import pymysql
import os,json
import re
import traceback


answer_dir = r"D:\WORKSPACE\助教工作\作业批改\作业答案"
datadir = r"D:\WORKSPACE\助教工作\AssistantTeaching\usermanage\workdata_dir"
problem_dir = r"D:\WORKSPACE\助教工作\作业批改\作业题目"
def getDatabase():
    conn = pymysql.connect(
        host='localhost',user='root',passwd='lrr1996429',
        db='assistantteaching',charset='utf8'
    )
    return  conn

def closeDataBase(conn):
    conn.close()

def readFileList():
    file_list = os.listdir(datadir)
    # file_list = [os.path.join(datadir,file) for file in file_list]
    # print(file_list)
    return file_list

def insertData(file_list):
    sql = (
        "insert into score(stuNo,stuName,workName,workSubmit) "+
        " values ('%s', '%s', '%s', '{json}');"
    )
    conn = getDatabase()
    for file in file_list:
        file_path = os.path.join(datadir,file)
        with open(file_path,'r',encoding='utf8') as f:
            json_str = json.loads(f.read())

        json_str = json.dumps(json_str)
        print(type(json_str))
        file_split = re.split('[-,.]',file)
        f_stuNo = file_split[0]
        f_stuName = file_split[1]
        f_workName = file_split[2]

        data = (f_stuNo,f_stuName,f_workName)
        # print(sql%data)
        cursor = conn.cursor()
        try:
            tsql = sql%data
            tsql = tsql.format(json=pymysql.escape_string(json_str))
            cursor.execute(tsql)
            conn.commit()
        except:
            traceback.print_exc()
            conn.rollback()
        # print(file_split)

    closeDataBase(conn)

def readChoiceAnswer():
    file_list = os.listdir(answer_dir)
    # print(file_list)

    file_list = [file for file in file_list if len(file)<10]
    # print(file_list)
    path_list = [os.path.join(answer_dir,file) for file in file_list]
    # print(path_list)

    for i, file in enumerate(path_list):
        file_name = file_list[i].split('.')[0]
        # print(file_name)
        answer_dict = {}
        with open(file,'r',encoding='utf8') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]

        for line in lines:
            answer_list = line.split(" ")
            if len(answer_list) == 0 or len(answer_list[0]) ==0:
                continue
            # print(answer_list)
            answer_no = answer_list[0]
            answer_content = answer_list[1]

            answer_dict[answer_no] = answer_content

        # print(answer_dict)
        json_str = json.dumps(answer_dict,indent=2,ensure_ascii=False)
        sql = (
            "insert into answer(workName,workAnswer) "+
               " values('%s', '{json}');")
        t_sql = sql%file_name
        t_sql = t_sql.format(json=pymysql.escape_string(json_str))
        conn = getDatabase()
        cursor = conn.cursor()
        try:
            cursor.execute(t_sql)
            conn.commit()
        except:
            traceback.print_exc()
            conn.rollback()

        closeDataBase(conn)


def readProblem():
    file_list = []
    for file in os.listdir(problem_dir):
        name,type= os.path.splitext(file)
        if "txt" in type:
            file_list.append(file)

    path_list = [os.path.join(problem_dir,file) for file in file_list]

    for i,file in enumerate(path_list):
        file_name = file_list[i].split(".")[0]
        problem_dict = {}
        print(file_name)

        with open(file,'r',encoding='utf8') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]

        # print(lines)
        for line in lines:
            problem_list = line.split(" ")
            if len(problem_list) == 0 or len(problem_list[0]) == 0:
                continue
            # print(problem_list)
            problem_no = problem_list[0]
            problem_content = problem_list[1]

            problem_dict[problem_no] = problem_content
        # print(problem_dict)
        json_str = json.dumps(problem_dict,indent=2,ensure_ascii=False)
        sql = (
            "insert into problem (workname, wrokcontent) "+
            " values ('%s','{json}');"
        )
        t_sql = sql%file_name
        t_sql = t_sql.format(json=pymysql.escape_string(json_str))
        conn = getDatabase()
        cursor = conn.cursor()
        try:
            cursor.execute(t_sql)
            conn.commit()
        except:
            traceback.print_exc()
            conn.rollback()

        closeDataBase(conn)


if __name__ == '__main__':
    # file_list = readFileList()
    # insertData(file_list)
    readChoiceAnswer()
    # readProblem()