import socket
import threading
from typing import List, Tuple
from auction import AuctionConnectionManager, User, Auction, Bid

HOST = "127.0.0.1"
PORT = 8888

def handle_connection(conn: socket.socket, addr: Tuple[str, int],conn_manager: AuctionConnectionManager):
    with conn:
        while True:
            print("Waiting for a msg from ", addr, "...")
            msg = conn.recv(1024)
            if not msg:
                break
            print(msg.decode("utf-8"))
            print("Received")
            handle_msg(msg, conn_manager)

def handle_msg(msg, conn_manager):
    pass


if __name__ == "__main__":
    conn_manager = AuctionConnectionManager()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Listening on: ", HOST, PORT)
        while True:
            conn, addr = s.accept()
            print("Connected: ", conn, addr)
            threading.Thread(target=handle_connection, args=(conn, addr, conn_manager,)).run()


