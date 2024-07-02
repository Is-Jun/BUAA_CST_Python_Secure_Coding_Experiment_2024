from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# 创建一个基类用于定义ORM模型类的基础
Base = declarative_base()


# 定义ORM类，用于映射students表格
class Student(Base):
    __tablename__ = 'students'  # 定义ORM类的映射表格名称
    id = Column(Integer, primary_key=True)  # 定义表格列，id作为主键
    name = Column(String(50))  # name列，存储学生姓名，数据类型为字符串
    mail = Column(String(50))  # mail列，存储学生邮箱
    password = Column(String(20), default='123456')  # 口令，默认为123456


# 定义ORM类，用于映射course表格
class Course(Base):
    __tablename__ = 'course'  # 定义ORM类的映射表格名称
    id = Column(Integer, primary_key=True)  # 定义表格列，id作为主键
    name = Column(String(50))  # name列，存储课程名称


# 添加学生信息到数据库
def add_student(session, name, mail=None, password=None):
    new_student = Student(name=name, mail=mail, password=password)
    session.add(new_student)
    session.commit()


# 添加课程信息到数据库
def add_course(session, name):
    new_course = Course(name=name)
    session.add(new_course)
    session.commit()


# 查询学生信息
def get_student(session, name):
    return session.query(Student).filter_by(name=name).first()


# 查询课程信息
def get_course(session, name):
    return session.query(Course).filter_by(name=name).first()


# 关闭数据库会话，释放数据库链接资源
def close_session(session):
    session.close()


def main():
    # 创建一个Engine对象，指定数据库连接字符串
    engine = create_engine('mysql+pymysql://root:**@127.0.0.1/Python-test')

    # 尝试连接数据库
    try:
        connection = engine.connect()
        print("数据库连接成功")
        connection.close()
    except Exception as e:
        print("数据库连接失败：", e)


    Base.metadata.create_all(engine)  # 创建所有定义的数据库表
    Session = sessionmaker(bind=engine)  # 创建一个会话，并绑定已建立的数据库引擎
    session = Session()  # 创建一个数据库会话对象，用于执行数据库操作
    try:
        add_student(session, '小明')
        add_course(session, 'Python安全编程')
        student = get_student(session, '小明')
        course = get_course(session, 'Python安全编程')

        print(f'Student: ID:{student.id}, Name:{student.name}')
        print(f'Course: ID:{course.id}, Name:{course.name}')

        close_session(session)
    except Exception as e:
        print(e)
        close_session(session)


if __name__ == '__main__':
    main()
