class Record:

    # __slots__ 包含的必须是 instance variable, class variable 不行
    __slots__ = ["name", "age", "skill"]

    def __init__(self, name, age, skill):
        self.name = name
        self.age = age
        self.skill = skill

    def show(self):
        print(self.name, self.age, self.skill)

    # 使用 __slots__ 之后，不能在增加 instance variable，比如下面的方法调用的时候会出错
    def set_male(self, gender):
        self.gender = gender

    def set_skill(self, skill):
        self.skill = skill


if __name__ == '__main__':
    a = Record("wangmeng", "28", "read")
    a.show()
    # 还是可以改 instance attribute 的
    a.set_skill("thinking")
    a.show()
    # 下面这一步会报错，因为定义了 __slots__ 之后， instance attribute 只能是 __slots__ 定义的那么多了
    a.set_male("男")
