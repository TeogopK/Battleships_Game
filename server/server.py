import socket
from _thread import *

server = "192.168.142.49"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


def threaded_client(conn):
    conn.send(str.encode("Connected"))
    reply = ""
    received = ''

    while True:
        try:
            data = conn.recv(2048)
            received = data.decode("utf-8")

            reply = 'Obi wan'

            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", received)
                print("Sending : ", reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn,))
