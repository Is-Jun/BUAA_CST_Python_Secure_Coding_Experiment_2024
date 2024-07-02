import psutil
import datetime


def collect_system_information():
    system_information = {}

    # CPU信息
    cpu_times = psutil.cpu_times_percent(interval=1, percpu=False)
    try:
        system_information['CPU'] = {
            'User Time': cpu_times.user,  # 用户时间进程百分比
            'System Time': cpu_times.system,  # 内核进程和终端的时间百分比
            'Wait IO': cpu_times.iowait,  # 由于IO等待使CPU处于空闲状态的时间百分比
            'Idle': cpu_times.idle  # CPU处于空闲状态的时间百分比
        }
    except AttributeError as e:
        system_information['CPU'] = {
            'User Time': cpu_times.user,
            'System Time': cpu_times.system,
            'Wait IO': 'Windows系统无法获得',
            'Idle': cpu_times.idle
        }

    # 内存信息
    memory_info = psutil.virtual_memory()
    swap_memory = psutil.swap_memory()
    try:
        system_information['Memory'] = {
            'Total': memory_info.total,  # 内存总数S
            'Used': memory_info.used,  # 已使用的内存数
            'Free': memory_info.free,  # 空闲内存数
            'Buffers': str(memory_info.buffers),  # 缓冲使用数(为与下格式相匹配)
            'Cache': str(memory_info.cached),  # 缓存使用数
            'Swap': swap_memory.used  # 交换分区使用数
        }
    except AttributeError as e:
        system_information['Memory'] = {
            'Total': memory_info.total,
            'Used': memory_info.used,
            'Free': memory_info.free,
            'Buffers': 'Windows系统无法获得',
            'Cache': 'Windows系统无法获得',
            'Swap': swap_memory.used
        }

    # 磁盘信息
    disk_info = psutil.disk_io_counters()
    system_information['Disk'] = {
        'read_count': disk_info.read_count,  # 读IO数
        'write_count': disk_info.write_count,  # 写IO数
        'read_bytesIO': disk_info.read_bytes,  # 读字节数
        'write_bytesIO': disk_info.write_bytes,  # 写字节数
        'read_time': disk_info.read_time,  # 磁盘读时间
        'write_time': disk_info.write_time  # 磁盘写时间
    }

    # 网络信息
    network_info = psutil.net_io_counters()
    system_information['Network'] = {
        'bytes_sent': network_info.bytes_sent,  # 发送字节数
        'bytes_recv': network_info.bytes_recv,  # 接收字节数
        'packets_sent': network_info.packets_sent,  # 发送数据包数
        'packets_recv': network_info.packets_recv  # 接收数据包数
    }

    # 用户信息
    users_info = psutil.users()
    system_information['Users'] = [{'name': user.name,  # 用户名
                                    'terminal': user.terminal  # 用户登录使用的终端设备
                                    } for user in users_info]

    # 其他信息
    boot_time = psutil.boot_time()
    system_information['Other'] = {
        'Boot Time': datetime.datetime.fromtimestamp(boot_time).strftime("%Y-%m-%d %H:%M:%S"),  # 开机时间
        'Uptime': datetime.timedelta(seconds=int(datetime.datetime.now().timestamp() - boot_time))  # 系统运行时间
    }

    return system_information


def write_to_file(data: dict):
    with open('system_information.txt', 'w', encoding='utf-8') as f:
        for category, info in data.items():
            f.write(f'{category}:\n')
            if type(info) == list:  # 用户信息为一个列表
                for item in info:
                    for key, value in item.items():
                        f.write(f'\t{key}:  {value}\n')
            else:
                for key, value in info.items():
                    f.write(f'\t{key}:  {value}\n')
            f.write('\n\n')


if __name__ == '__main__':
    system_information = collect_system_information()
    write_to_file(system_information)
