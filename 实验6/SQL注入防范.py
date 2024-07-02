from sqlalchemy import create_engine, MetaData, Table, Column, Integer , String, text
from sqlalchemy.exc import IntegrityError

# 创建数据库引擎，连接到student-test，不启用SQL语句输出
engine = create_engine('mysql+pymysql://root:*@127.0.0.1/student-test', echo=False)

# 创建元数据对象，用于跟踪数据表结构
metadata = MetaData()

# 创建数据表格对象students，包括id、username、password和mail列
students = Table(
    'students',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(50)),
    Column('password', String(50)),
    Column('mail', String(50), unique=True)
)

# 如果不存在，创建数据库表格
metadata.create_all(engine)

# 插入数据，使用text函数来插入两条记录，邮箱包含“qq.com”
insert_queries = [
    text("INSERT INTO students (username, password, mail) VALUES (:username1, :password1, :mail1)").
    params(username1='小明', password1='123456', mail1='xiaoming@qq.com'),
    text("INSERT INTO students (username, password, mail) VALUES (:username2, :password2, :mail2)").
    params(username2='小红', password2='654321', mail2='xiaohong@qq.com')
]

# 插入数据：循环执行数据插入，并检查邮箱的唯一性
try:
    # 使用数据库引擎创建一个连接上下文
    with engine.connect() as conn:
        for query in insert_queries:
            conn.execute(query)
        # 提交事务，将更改保存到数据库
        conn.commit()
except IntegrityError as e:
    error_message = str(e)
    # 捕获完整性错误，判断是否违反唯一约束
    if 'Duplicate entry' in error_message:
        print("该邮箱已存在，请输入其他邮箱。")
    else:
        print("发生完整性错误：", error_message)

# 查询数据：使用text函数执行原始SQL查询，查找邮箱包含“qq.com”的学生记录
select_query = text("SELECT * FROM students WHERE mail LIKE :pattern").params(pattern='%qq.com%')

# 使用数据库引擎连接到数据库，并创建一个上下文管理器，确保在退出时自动关闭连接
with engine.connect() as conn:
    # 执行SQL查询，将查询结果存储在result中
    result = conn.execute(select_query)
    # 获取查询表格的列名
    columns = result.keys()

    # 遍历查询结果集合并打印每条记录
    for row in result:
        # 将每一行结果转换为字典，其中字典的键是列名，值是对应的数据
        student_dict = dict(zip(columns, row))
        # 打印学生记录的信息，包括id、username和mail
        print(f"Student ID:{student_dict['id']}, username:{student_dict['username']}, Mail:{student_dict['mail']}")
