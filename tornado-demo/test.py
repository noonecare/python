from requests import get
from multiprocessing import Pool


if __name__ == '__main__':
    my_pool = Pool(100)
    my_pool.map(get, ["http://localhost:4000"] * 100)
