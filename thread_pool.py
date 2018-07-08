"""
    自己用 python 实现 thread pool。
"""

from threading import Thread
from queue import Queue


# 使用 queue 传递参数（自己实现参数传递太复杂了。
# todo: 阅读 queue 的源码，了解 queue 的原理。）

class MyExecutor(Thread):
    def __init__(self, q, pool, result_q):
        self._q = q
        self._result_q = result_q
        self._pool = pool
        super().__init__()

    def run(self):
        while True:
            func, args, kwargs = self._q.get()
            # 使用 executor 执行传递过来的任务。
            # 并把执行结果放在 _result_q 中传递出去。
            result = func(*args, **kwargs)
            self._q.task_done()
            self._result_q.put(result)
            # 执行完任务之后，把当前线程放回线程池中。
            self._pool.add(self)

    # 通过向 queue 中添加任务，使得进程池执行该任务。
    def __call__(self, func, *args, **kwargs):
        # 每个线程独享一个 task_queue 和 result_queue 确
        # 保了，当前 return 的值，就是当前 call 的值。否
        # 则顺序可能会乱掉。
        self._q.put((func, args, kwargs))
        return self._result_q.get()


class MyThreadPool(set):
    def __init__(self, size):
        for _ in range(size):
            q = Queue()
            result_queue = Queue()
            t = MyExecutor(q, self, result_queue)
            # 把 executor 设成 daemon。
            t.setDaemon(True)
            t.start()
            self.add(t)

    def get_thread(self):
        # 拿出 Executor 来执行任务。
        return self.pop()


def test_MyThreadPool():
    def add_(a, b):
        return a + b

    def minus_(a, b):
        return a - b

    def times_(a, b):
        return a * b

    def div_(a, b):
        return a / b

    pool = MyThreadPool(2)

    t = pool.get_thread()

    print(t(add_, 2, 3))
    print(t(minus_, 2, 3))
    print(t(times_, 2, 3))
    print(t(div_, 2, 3))
