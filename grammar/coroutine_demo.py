"""
石头剪子布游戏
"""
import random


cards = dict(zip([2, 1, 0], ["石头", "剪子", "布"]))


def a_player():
    yield random.randint(0, 2)


def b_player():
    yield random.randint(0, 2)

a_wins = 0
b_wins = 0


def referee(a, b):
    global a_wins, b_wins
    if a == b:
        yield
    if a == b + 1:
        a_wins += 1
        yield
    if a == b + 2:
        b_wins += 1
        yield
    if a == b - 1:
        b_wins += 1
        yield
    if a == b - 2:
        a_wins += 1
        yield


def play_game(count=10):
    global a_wins, b_wins
    a_wins = 0
    b_wins = 0
    for i in range(count):
        a = next(a_player())
        b = next(b_player())
        next(referee(a, b))
        print("a is {a}".format(a=cards[a]))
        print("b is {b}".format(b=cards[b]))
        print("当前比分 {a_wins}: {b_wins}".format(a_wins=a_wins, b_wins=b_wins))


if __name__ == '__main__':
    play_game(10)

