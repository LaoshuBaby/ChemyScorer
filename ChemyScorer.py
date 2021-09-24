###### IMPORT
import os
import sqlite3

###### GLOBAL
GLOBAL_MODE = 0


###### Database Operation

def Insert():
    return 1


def Put():
    return 1


###### MODE CHANGE
print("请输入您希望进入的模式")
print("1.动员模式")
print("2.录入模式")
print("3.汇总模式")
print("4.退出程序")

GLOBAL_MODE = input()

def MODE_TASK():
    return 0


def MODE_INPUT():
    return 0


def MODE_MERGE():
    return 0

while True:
    if eval(GLOBAL_MODE) == 1:
        MODE_TASK()
    elif eval(GLOBAL_MODE) == 2:
        MODE_INPUT()
    elif eval(GLOBAL_MODE) == 3:
        MODE_MERGE()
    else:
        print("EXIT")
        break
quit(0)

###### INIT
print("请输入总共的学生人数")
num_stu = int(input())
list_global = []
print("1.接下来输入时中间必须用英文逗号分割")
print("2.题目分数必须严格按照顺序执行，没有分数的题目需要写0分")
print("3.总题目数量可自动识别，保证执行过程中一致即可")
print("4.如果输入到一半不想输入了，就输入000000打断程序")
print("样例：  114,5,1,4,1,9,1,9,8,1,0")
print("5.每次使用前输出文件不能在使用中")
print("\n")

###### INPUT
for i in range(num_stu):
    print("==请输入一个学生的学号和各题目成绩==")
    str_input = input()
    if str_input != "000000":
        ## SPACE
        str_input = str_input.replace(" ", ",")
        ## CHINESE SYNTAX
        str_input = str_input.replace("，", ",")
        str_input = str_input.replace("。", ".")
        ## SPECIAL SYNTAX
        str_input = str_input.replace(".,", ".5,")
        str_input = str_input.replace("q", ".5")
        list_score = str_input.split(",")
        for j in range(len(list_score)):
            if j == 0:
                list_score[j] = int(list_score[j])
            else:
                list_score[j] = float(list_score[j])
        list_global.append(list_score)
        print("学号为", list_score[0], "的学生已经记录")
    else:
        break

###### OUTPUT
ospath = os.path.join(os.path.expanduser("~"), "Desktop") + "\\test_score.csv"
outputfile = open(ospath, "w")
### HEAD
temp_str_head = "\"学号\""
for i in range(len(list_global[0]) - 1):
    temp_str_head += ",\"第"
    temp_str_head += str(i + 1)
    temp_str_head += "题\""
outputfile.write(temp_str_head + "\n")
del temp_str_head
### BODY
for i in range(len(list_global)):
    temp_str = str(list_global[i][0])
    for j in range(len(list_global[i]) - 1):
        temp_str += ","
        temp_str += str(list_global[i][j + 1])
    outputfile.write(temp_str + "\n")
### FINISH
outputfile.close()
