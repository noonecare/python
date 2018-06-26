"""
文件记录了 开始ip:结束ip：联通还是不联通。
给定一个 ip, 判断该 ip 是否联通。

内存最多给 1G。

这里 1G 是个明显的提示。没发现这个问题，说明我平时不够关注空间复杂度。
"""
import numpy as np


def _ip_to_long(ip):
    a, b, c, d = ip.split('.')
    return int(a) * 256 * 256 * 256 + int(b) * 256 * 256 + int(c) * 256 + int(d)


connect_buffer = np.zeros(2 ** 32)


def _record_connect_state_to_connect_buffer(start_ip, end_ip):
    start_ip = _ip_to_long(start_ip)
    end_ip = _ip_to_long(end_ip)
    for i in range(start_ip, end_ip + 1):
        connect_buffer[i] = 1


def preprocess(ip_connect_file):
    with open(ip_connect_file, 'rt', encoding='utf-8') as f:
        for line in f:
            start_ip, end_ip, _ = line.split(',')
            _record_connect_state_to_connect_buffer(start_ip, end_ip)


preprocess(ip_connect_file="your_ip_connect_file")


def is_ip_connect(ip):
    return bool(connect_buffer[ip])
