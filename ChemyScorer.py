###### IMPORT
import os
import sqlite3

###### GLOBAL
global GLOBAL_DEBUG
global GLOBAL_MODE

global GLOBAL_TASK_NAME
global GLOBAL_QUESION_NUM
global GLOBAL_FORCE_REVIEW_MEMBER
global GLOBAL_FORCE_REVIEW_TIME

GLOBAL_DEBUG = 1
GLOBAL_MODE = 0


###### LIB_FUNC

def replaceX(src, A, B):
    if A in src:
        if GLOBAL_DEBUG == 1:
            print("In", src, "Find\"", A, "\"--->\"", B, "\"")
        src = src.replace(A, B)
    return src


###### Database Operation

def PUSH(DATABASE, TABLE_NAME, SQL="", DATA_LIST=[]):
    if TABLE_NAME == 0:
        # EXECUTE SQL
        CURSOR = DATABASE.cursor()
        CURSOR.execute(SQL)
        CURSOR.close()
        DATABASE.commit()
    else:
        # INIT
        SQL = ""
        SQL_LEADING = "INSERT INTO " + TABLE_NAME + " VALUES ("
        SQL_COMMA = ", "
        SQL_END = ");"
        # START
        SQL += SQL_LEADING
        for i in range(len(DATA_LIST)):
            if DATA_LIST[i][1] == "INT" or DATA_LIST[i][1] == "FLOAT":
                SQL += str(DATA_LIST[i][0])
                if i != (len(DATA_LIST) - 1):
                    SQL += SQL_COMMA
            elif DATA_LIST[i][1] == "STRING":
                SQL += "'" + DATA_LIST[i][0] + "'"
                if i != (len(DATA_LIST) - 1):
                    SQL += SQL_COMMA
            else:
                SQL += "'" + DATA_LIST[i][0] + "'"
                if i != (len(DATA_LIST) - 1):
                    SQL += SQL_COMMA
        SQL += SQL_END
        if GLOBAL_DEBUG == 1:
            print(SQL)
        CURSOR = DATABASE.cursor()
        CURSOR.execute(SQL)
        CURSOR.close()
        DATABASE.commit()
    return 1


def POP(DATABASE, TABLE_NAME, SQL):
    return 1


def SWAP(A, B):
    if A[0] < B[0]:
        return [A, B]
    else:
        return [B, A]


###### MODE_FUNC


def MODE_CREATE():
    STEP = 1
    ## TASK_NAME
    print("==STEP", STEP, "请输入本次待录入成绩的考试名称==")
    print("1.推荐仅包含英文数字下划线")
    print("2.不建议出现横线空格和中文")
    GLOBAL_TASK_NAME = input()
    STEP += 1
    ## QUESION_NUM
    print("==STEP", STEP, "请输入本次考试共有多少题目==")
    GLOBAL_QUESION_NUM = int(input())
    if GLOBAL_QUESION_NUM <= 0:
        return "ERROR_NONEXIST_QUANTITY"
    STEP += 1
    ## FORCE_REVIEW_MEMBER
    print("==STEP", STEP, "录入过程是否强制签名==")
    print("1.强制签名填1或True，否则填0或False")
    print("2.大小写敏感")
    GLOBAL_FORCE_REVIEW_MEMBER = input()
    STEP += 1
    ## FORCE_REVIEW_TIME
    print("==STEP", STEP, "录入过程是否强制记录瞬间时间==")
    print("1.强制记录时间填1或True，否则填0或False")
    print("2.大小写敏感")
    GLOBAL_FORCE_REVIEW_TIME = input()
    STEP += 1
    ## WRITE
    DATABASE = sqlite3.connect(str(GLOBAL_TASK_NAME) + ".db")
    SQL_init_BODY = "CREATE TABLE \"BODY\" (" \
                    "\"STU_NUMBER\" integer NOT NULL," \
                    "\"SCORE_LIST\" TEXT(255) NOT NULL," \
                    "\"REVIEW_MEMBER\" TEXT(255)," \
                    "\"REVIEW_TIME\" TEXT(255)," \
                    "PRIMARY KEY (\"STU_NUMBER\")" \
                    ");"
    SQL_init_HEAD = "CREATE TABLE \"HEAD\" (" \
                    "\"TASK_NAME\" text(255) COLLATE BINARY," \
                    "\"QUESTION_NUM\" integer," \
                    "\"FORCE_REVIEW_MEMBER\" text(255)," \
                    "\"FORCE_REVIEW_TIME\" text(255)" \
                    ");"
    PUSH(DATABASE, 0, SQL_init_BODY)
    PUSH(DATABASE, 0, SQL_init_HEAD)
    DATA_LIST_INIT = []
    DATA_LIST_INIT.append([GLOBAL_TASK_NAME, "STRING"])
    DATA_LIST_INIT.append([GLOBAL_QUESION_NUM, "INT"])
    DATA_LIST_INIT.append([GLOBAL_FORCE_REVIEW_MEMBER, "STRING"])
    DATA_LIST_INIT.append([GLOBAL_FORCE_REVIEW_TIME, "STRING"])
    PUSH(DATABASE, "HEAD", "", DATA_LIST_INIT)
    ## FINISH
    DATABASE.commit()
    DATABASE.close()
    return 0


def MODE_INPUT():
    ## STEP1
    STEP = 1
    print("==STEP", STEP, "请输入本次待录入成绩的考试名称==")
    print("1.推荐仅包含英文数字下划线")
    print("2.不建议出现横线空格和中文")
    print("3.输入000000则选择已有考试文件")
    GLOBAL_TASK_NAME = input()
    STEP += 1
    if GLOBAL_TASK_NAME != "000000":
        DATABASE = sqlite3.connect(str(GLOBAL_TASK_NAME) + ".db")
        # 然后把TASKNAME自动塞进去
    else:
        # 后期GUI界面需要给一个可选择的
        print("请选择需要打开的文件")
        GLOBAL_DBNAME = input()
        DATABASE = sqlite3.connect(str(GLOBAL_DBNAME) + ".db")
    ## STEP2
    CURSOR_select_force_review_member = DATABASE.cursor()
    SQL_select_force_review_member = "SELECT FORCE_REVIEW_MEMBER FROM HEAD"
    CURSOR_select_force_review_member.execute(SQL_select_force_review_member)
    GLOBAL_FORCE_REVIEW_MEMBER = CURSOR_select_force_review_member.fetchone()[0]
    CURSOR_select_force_review_member.close()
    if GLOBAL_FORCE_REVIEW_MEMBER == "True" or GLOBAL_FORCE_REVIEW_MEMBER == 1 or GLOBAL_FORCE_REVIEW_MEMBER == "1":
        print("==STEP", STEP, "请输入录入人员的姓名==")
        GLOBAL_TASKNAME = input()
        STEP += 1
    ## STEP3
    print("==STEP", STEP, "请输入预计本次录入的学生人数==")
    STU_NUM = int(input())
    if STU_NUM <= 0:
        return "ERROR_NONEXIST_QUANTITY"
    list_global = []

    print("1.接下来输入时中间必须用英文逗号分割")
    print("2.题目分数必须严格按照顺序执行，没有分数的题目需要写0分")
    print("3.总题目数量可自动识别，保证执行过程中一致即可")
    print("4.如果输入到一半不想输入了，就输入000000打断程序")
    print("5.每次使用前输出文件不能在使用中")
    print("样例（标准输入）：  114,5.5,1,4,1,9,1,9,8,1,0")
    print("样例（快速注记）：  114c5q1s4s1s9s1s9s8s1s0s")
    print("\n")

    ###### INPUT
    for i in range(STU_NUM):
        print("==请输入一个学生的学号和各题目成绩==")
        str_input = input()
        if str_input != "000000":
            ## SPACE
            str_input = replaceX(str_input, " ", ",")
            ## CHINESE SYNTAX
            str_input = replaceX(str_input, "，", ",")
            str_input = replaceX(str_input, "。", ".")
            ## SPECIAL SYNTAX
            str_input = replaceX(str_input, ".,", ".5,")
            str_input = replaceX(str_input, "q,", ".5,")
            ## FAST SYNTAX
            str_input = replaceX(str_input, "q", ".5,")  # 小数分数
            str_input = replaceX(str_input, "c", ",")  # 学号
            str_input = replaceX(str_input, "s", ",")  # 整数分数
            ## BUG FIX
            str_input = str_input.replace(",,", ",")
            if str_input[len(str_input) - 1] == ",":
                str_input = str_input[0:len(str_input) - 1]
            if GLOBAL_DEBUG == 1:
                print(str_input)
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
    print("已结束本次录入")
    outputfile.close()
    DATABASE.commit()
    DATABASE.close()
    return 0


def MODE_MERGE():
    STEP = 1
    print("==STEP", STEP, "请输入预计本次合并的文件个数==")
    FILE_NUM = int(input())
    if FILE_NUM <= 0:
        return "ERROR_NONEXIST_QUANTITY"
    FILE_LIST = []
    for i in range(FILE_NUM):
        print("==请选择第", i + 1, "个文件的位置==")
        FILE_LIST.append(input())
    ## 开始逐个文件读取然后记录数据库
    for i in range(FILE_LIST):
        print("文件记载到库里了")
    ## 合并输出文件，在这之前需要先排序
    ## 造一个comp函数，对多个结构体排序
    # TEMP = SWAP(A0, B0)
    # A0 = TEMP[0]
    # B0 = TEMP[1]
    # del TEMP
    ## 排序后逐个扫，得到学号最大值
    # ## 然后range(STU_NUMBER_MAX)以后对缺失的插值补齐
    # for i in range(STU_NUMBER_MAX):
    #     flag_EXIST = 0
    #     TEMP_ROW=[]
    #     TEMPLETE_NULL=[0,"0",0,0]
    #     for j in range(len(SCORE_RAW)):
    #         if SCORE_RAW[j][0]==i:
    #             flag_EXIST=1
    #             TEMP_ROW=SCORE_RAW[j]
    #     if flag_EXIST==1:
    #         STU_NUMBER_FULL[i]=TEMP_ROW
    #     else:
    #         STU_NUMBER_FULL[i]=TEMPLETE_NULL
    # ## 然后STU_NUMBER_FULL就是拍好了可以输出的那个
    return -1


###### MAIN


while True:
    print("==请输入您希望进入的模式==")
    print("(不输入或异常输入均会退出)")
    print("1.创建考试")
    print("2.录入模式")
    print("3.汇总模式")
    print("4.退出程序")
    GLOBAL_MODE = input()
    if eval(GLOBAL_MODE) == 1:
        TEMP_RETURN = MODE_CREATE()
    elif eval(GLOBAL_MODE) == 2:
        TEMP_RETURN = MODE_INPUT()
    elif eval(GLOBAL_MODE) == 3:
        TEMP_RETURN = MODE_MERGE()
    else:
        TEMP_RETURN = 0
        print("EXIT")
        break
if GLOBAL_MODE == 1 and TEMP_RETURN == "ERROR_NONEXIST_QUANTITY":
    print("退出原因：不存在的数量")
if GLOBAL_MODE == 2 and TEMP_RETURN == "ERROR_NONEXIST_QUANTITY":
    print("退出原因：不存在的数量")
if GLOBAL_MODE == 3 and TEMP_RETURN == "ERROR_NONEXIST_QUANTITY":
    print("退出原因：不存在的数量")
quit(0)
