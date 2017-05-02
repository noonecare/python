class Shop:
    def __enter__(self):
        print("客官，里面请")

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("谢谢惠顾")


if __name__ == '__main__':
    with Shop():
        pass
