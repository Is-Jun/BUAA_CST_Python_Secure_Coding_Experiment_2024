from concurrent.futures import ThreadPoolExecutor  # 用于创建线程池以执行并发任务
import requests
import threading
import urllib3
import random

# 常见的文件扩展名，可能与备份或归档文件相关
extension_name = ['.bak', '.nr', '.7z', '.swp', '.tar.gz', '.zip', ',jsp']

# 定义一个线程锁对象，用于同步访问共享资源
write_file_lock = threading.Lock()

# 指定可以由ThreadingPoolExecutor创建的最大线程数
MAX_THREADS = 64

# 包含可以随请求发送的HTTP头
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"}

# 禁用了使用requests发送不安全HTTP请求时引发的警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def url_generator(domin, dictfile):
    with open(dictfile, 'r', encoding='utf-8') as f:
        for line in f:
            # 去除行首尾的空格和斜杠
            word = line.strip().strip('/')
            yield f'{domin}/{word}'  # 生成URL
            # 如果单词中不包含“.”，则再为每个单词添加扩展名后生成对应的URL
            if '.' not in word:
                for ex in extension_name:
                    yield f"{domin}/{word}{ex}"


def url_test(url, f):  # 测试给定的URL是否可以访问，并将结果写入文件
    try:
        # 发起GET请求，获取URL的相应
        req = requests.get(url, headers=headers, verify=False)
        # 如果状态码不是404，即页面存在，将URL写入文件
        if req.status_code != 404:
            # 使用互斥锁，确保多线程下的文件写入操作是安全的
            write_file_lock.acquire()
            # 打印状态码和URL
            print(f'[{req.status_code}]==>{url}')
            f.write(url + '\n')
            write_file_lock.release()
        return 0
    except Exception as e:
        # 打印异常信息，通常是网络连接问题或其他异常
        print(e)
        return -1


def run_tasks_threads(domin, dictfile, resultfile):  # 多线程任务运行
    # 创建一个URL生成器对象
    url_gen = url_generator(domin, dictfile)
    with open(resultfile, 'w', encoding='utf-8') as f:
        # 使用ThreadPoolExecutor类创建一个线程池对象，该对象最多可以同时运行MAX_THREADS个线程
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            while True:
                try:
                    # 调用next()从url_gen获取下一个URL
                    url = next(url_gen)
                    # 创建一个新的线程来测试URL
                    executor.submit(url_test, url, f)
                except StopIteration as si:
                    # 发生StopIteration异常说明已经遍历完所有的URL，可以退出循环
                    break


def get_dict_test(dict_list, dictionary, x):  # 输入一个个字典文件列表，返回一个数据量为其x%的字典
    with open(dictionary, 'w', encoding='utf-8') as F:
        for dict in dict_list:
            with open(dict, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                l = len(lines)
                num = []
                for i in range(l // 100 * x):
                    n = random.randint(0, l - 1)
                    if n not in num:
                        num.append(n)
                        F.write(lines[n])


def main():
    domin = 'http://testfire.net'
    dictfile = 'dict-test.txt'  # 字典内容过多运行时间过慢，选取不同字典各自的x%做成测试集
    get_dict_test(['DIR.txt', 'word-frequency.txt', 'sensitive.txt'], dictfile, 5)
    resultfile = 'result.txt'

    run_tasks_threads(domin, dictfile, resultfile)


if __name__ == '__main__':
    main()
