"""
    自定义 thread pool。
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    1. 使用 Queue 在主线程和 Executor 之间传递参数。（自己实现线程间通
    讯是很难的，而且每种语言几乎都自带了实现线程间通信的 API, 使用现成
    的 API 是最优的实现。有空读读 Queue 的源码，加深对于线程间通讯的理
    解。）

    2. 这个实现，没有给出线程调度机制。把多线程拆成 Executor 和 Task
    两个概念，就是为了方便地使用不同的线程调度机制。所以这个实现，只是
    个练习。实际编程不要使用这个 `MyThreadPool`。

    3. 这个实现，控制了线程池的大小，复用线程（节约了线程创建的时间），
    提高了效率。
"""

from threading import Thread
from queue import Queue


class MyExecutor(Thread):
    def __init__(self, task_q, result_q, pool):
        self._q = task_q
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
            task_q = Queue()
            result_q = Queue()
            t = MyExecutor(task_q, result_q, self)
            # 把 executor 设成 daemon。
            t.setDaemon(True)
            t.start()
            self.add(t)

    def get_thread(self):
        # 拿出 Executor 来执行任务。
        return self.pop()


def test_case():
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
