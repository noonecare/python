"""
验证 accept 得到的是 connection， 不是消息 
"""

from socket import socket, AF_INET, SOCK_STREAM


def pick_a_message(conn):
    msg = ""
    data = conn.recv(1024)
    data = data.decode("utf-8")
    while not data.endswith("\n"):
        msg = msg + data
        data = conn.recv(1024)
        data = data.decode("utf-8")
        print(data)
    msg = msg + data
    return msg


def start_socket_server(HOST, PORT, backlog=2):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((HOST, PORT))
    # listen 侦听端口，从此 这个端口变成了服务器
    # 不 listen 不能成为服务器
    # 最多侦听 backlog 个 connection
    s.listen(backlog)
    # 依次处理每个 connection
    while True:
        # accept 的作用是接受新的连接（新的链接是个没有绑定端口的socket）, accept 的返回值是新创建的连接（socket) 和 客户端的地址
        conn, address = s.accept()
        # 如果一个 connection 要收发多条信息，需要自己定义号分隔符。以及处理逻辑。
        # 每个 socket 看到的只是 BytesStream。
        # 当用户输入 quit 时，跳出循环
        while True:
            msg = pick_a_message(conn)
            print(msg)
            if msg.endswith("quit\n"):
                conn.close()
                break
            else:
                conn.sendall(msg.encode("utf-8"))


if __name__ == '__main__':
    start_socket_server("localhost", 8000)

