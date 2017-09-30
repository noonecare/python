# coding: utf-8
from threading import Thread, Event
from time import sleep


class StoppableThread(Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


def timeout(seconds):
    """
    :param seconds: timeout 秒数。如果修饰的函数经过 timeout 秒还没有运行结束，会报 Timeout 错误。
    """
    def timeout_decorator(func):
        def decorated_function(*args, **kwargs):
            t = StoppableThread(target=func, args=(*args,))
            t.setDaemon(True)
            t.start()
            sleep(seconds)
            if t.is_alive():
                t.stop()
                raise TimeoutError("timeout")

        return decorated_function

    return timeout_decorator


@timeout(30)
def f():
    """
    定义 f 函数是为了测试 timeout decorator 可以如预期那样地工作
    """

    while True:
        print("once again")
        sleep(10)


if __name__ == '__main__':
    f()
