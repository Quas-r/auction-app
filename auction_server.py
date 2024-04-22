import socket
import json
import threading
from typing import List, Tuple, Dict
from auction import AuctionConnectionManager, User, Auction, Bid

HOST = "127.0.0.1"
PORT = 8888
auctions: Dict[str, Auction] = {"3ab496a1-e504-457d-9598-a97209105a19": Auction("3ab496a1-e504-457d-9598-a97209105a19", User("Murat", "test", ("127.0.0.1", 6969)), "Auction 1", 120, [], None, True, None)}
auction_connections: Dict[str, List[User]] = {}

def handle_connection(conn: socket.socket, addr: Tuple[str, int]):
    with conn:
        while True:
            print("Waiting for a msg from ", addr, "...")
            msg_bytes = conn.recv(1024)
            if not msg_bytes:
                break
            print(msg_bytes.decode("utf-8"))
            print("Received")
            handle_msg(conn, addr, msg_bytes)

def handle_msg(conn: socket.socket, addr: Tuple[str, int], msg_bytes: bytes):
    msg = json.loads(msg_bytes.decode("utf-8"))[0]
    if msg["sender"] != "client":
        return
    content = msg["content"]
    if msg["msg_type"] == "connect_user_to_auction":
        usr = User(**content["user"], address=addr)
        add_user_to_auction(usr, content["auction_id"])
        auction = auctions.get(content["auction_id"])
        if auction:
            msg = {
                    "sender": "server",
                    "msg_type": "auction_info",
                    "content": {
                        "auction_id": auction.auction_id,
                        "owner": auction.owner.name,
                        "item_name": auction.item_name,
                        "starting_price": auction.starting_price,
                        "bids": [bid.__dict__ for bid in auction.bids],
                        "deadline": auction.deadline,
                        "open": auction.open,
                        "buyer": auction.buyer.name if auction.buyer else None
                        }
                    }
            conn.sendall(json.dumps(msg).encode("utf-8"))


def add_user_to_auction(usr: User, auction_id: str):
    if not auction_connections.get(auction_id):
        auction_connections[auction_id] = []
    if usr not in auction_connections[auction_id]:
        auction_connections[auction_id].append(usr)

def remove_user_from_auction(usr: User, auction_id):
    if not auction_connections.get(auction_id):
        return
    # if conn not in auction_connections[auction_id]:
    #     return
    auction_connections[auction_id].remove(usr)

if __name__ == "__main__":
    conn_manager = AuctionConnectionManager()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Listening on: ", HOST, PORT)
        while True:
            conn, addr = s.accept()
            print("Connected: ", addr)
            threading.Thread(target=handle_connection, args=(conn, addr,)).run()


