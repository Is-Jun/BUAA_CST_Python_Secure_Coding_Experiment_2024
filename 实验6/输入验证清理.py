import pymysql
import re
from pymysql.converters import escape_string

# 创建一个过滤表，包含不允许的关键字和字符
filter_table = {
    "single_quotes": r"'",      # 单引号
    "semicolon": r";",          # 分号
    "comment1": r"--",          # 注释符--
    "comment2": r"/\*.*\*/",    # 注释符/*……*/
    "union": r"UNION",          # 操作符UNION
    "or_operator": r"OR",       # 操作符OR
    "and_operator": r"AND",     # 操作符AND
    "delete": r"DELETE",        # DELETE语句
    "drop": r"DROP",            # DROP语句
    "percent": r"%"             # 百分号
}


def filter_input(input_str):
    # 使用正则表达式来检查输入，是否包含不被允许的关键字或字符
    for key, pattern in filter_table.items():
        # 全字符串中匹配过滤表中的关键字或字符，忽略大小写
        if re.search(pattern, input_str, re.IGNORECASE):
            # 如果发现不被允许的关键字或字符，抛出异常
            raise ValueError(f"Invalid input: {key} detected in input.")
    return input_str

# def filter_input(input_str):
#     # 使用正则表达式来检查输入，是否包含不被允许的关键字或字符
#     error = []
#     for key, pattern in filter_table.items():
#         # 全字符串中匹配过滤表中的关键字或字符，忽略大小写
#         if re.search(pattern, input_str, re.IGNORECASE):
#             # 如果发现不被允许的关键字或字符，抛出异常
#             if key not in error:
#                 error.append(key)
#     if error:
#         raise ValueError(f"Invalid input: {error} detected in input.")
#     return input_str


def insert_data(username, password):
    try:
        # 连接到数据库
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='*',
            database='student-test'
        )
        cursor = conn.cursor()  # 创建一个与数据库连接相关联的游标对象
        # 过滤输入的用户名和密码
        clean_username = filter_input(username)
        clean_password = filter_input(password)

        sql = f"INSERT INTO students (username, password) VALUES ('{clean_username}', '{clean_password}')"
        cursor.execute(sql)  # 将SQL查询语句发送到数据库服务器执行
        conn.commit()  # 将查询结果（更改）永久保存到数据库中
        print("Data inserted successfully!")
    except ValueError as e:  # 处理无效输入引发的异常
        print(f"Error:{e}")
    except Exception as e:  # 处理数据库操作引发的异常
        print(f"Database error:{e}")
    finally:
        cursor.close()
        conn.close()


def database_connect_test():
    try:
        # 连接到数据库
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='*',
            database='student-test'
        )
        print('Succeeded to connect to the database.')
        flag = False
    except Exception as e:  # 连接数据库失败
        print("Failed to connect to the database.")
        print(f'error_message: {e}')
        flag = True
    finally:
        conn.close()
        return flag


def main():
    if database_connect_test():  # 如果连接数据库失败
        return None
    print('Please enter the username and password you want to insert(enter the username as \'exit\' to exit)\n')
    while True:
        username = input("Please enter the username: ")
        if username == 'exit':
            break
        else:
            password = input("Please enter the password: ")
            print(f'Your input is: username: {username}, password: {password}')
            insert_data(username, password)


if __name__ == '__main__':
    main()
