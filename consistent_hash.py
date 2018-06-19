import numpy as np


class AlreadyBeenTaken(Exception):
    """这个槽位已经被占了，请换一个。"""


class NoCacheServer(Exception):
    """没有缓存服务器可用。"""


class ConsistentHash(object):

    def __init__(self, n):
        self._size = 2 ** n
        self._servers = np.zeros(self._size)
        self._redis_mapping = {}

    def _is_next(self, code_1, code_2):
        return (code_1 - code_2) % self._size <= self._size // 2

    def add_server(self, server_code, redis_instance):
        if self._servers[server_code]:
            raise AlreadyBeenTaken()

        self._servers[server_code] = 1

        # 缓存服务器迁移数据
        try:
            next = self._get_next_server(server_code)
            # 把 next 中会与 server_code 之前的缓存缓存到 redis_instance 中。
            for k in self._redis_mapping[next].keys():
                if self._is_next(server_code, k):
                    # 从原来的缓存服务器中删除该值
                    v = self._redis_mapping[next].get(k)
                    # todo: 确认这是不是根据 key 删除键值对
                    self._redis_mapping[next].delete(k)
                    redis_instance.set(k, v)

        except NoCacheServer:
            pass

        self._redis_mapping[server_code] = redis_instance

    def _get_next_server(self, key_code):
        for i in range(key_code, key_code + self._size):
            if self._servers[i % self._size] == 1:
                return i
        raise NoCacheServer()

    def set_cache(self, k, v):
        server_code = self._get_next_server(k)
        self._redis_mapping[server_code].set(k, v)

    def get_cache(self, k):
        server_code = self._get_next_server(k)
        return self._redis_mapping[server_code].get(k)
