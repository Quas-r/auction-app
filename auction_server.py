import socket
import json
import threading
from typing import List, Tuple, Dict
from auction import User, Auction, Bid

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
            handle_msg(conn, msg_bytes)

def handle_msg(conn: socket.socket, msg_bytes: bytes):
    msg = json.loads(msg_bytes.decode("utf-8"))
    if isinstance(msg, list):
        msg = msg[0]
    if msg["sender"] != "client":
        return
    content = msg["content"]
    if msg["msg_type"] == "connect_user_to_auction":
        usr = User(**content["user"], conn=conn)
        add_user_to_auction(usr, content["auction_id"])
        auction = auctions.get(content["auction_id"])
        if auction:
            send_auction_info(usr, auction)
    if msg["msg_type"] == "disconnect_user_from_auction":
        usr = User(**content["user"], conn=conn)
        remove_user_from_auction(usr, content["auction_id"])
    if msg["msg_type"] == "send_bid":
        usr = User(**content["bidder"], conn=conn)
        auction = auctions.get(content["auction_id"])
        users = auction_connections.get(content["auction_id"])
        if not auction:
            return
        bids = [ bid.amount for bid in auction.bids ]
        if len(bids) == 0:
            max_bid = auction.starting_price
        else:
            max_bid = max(bids)
        if content["amount"] <= max_bid:
            return
        if users and usr in users:
            auction.bids.append(Bid(content["auction_id"], usr, content["amount"]))
            for user in users:
                try:
                    send_auction_info(user, auction)
                except:
                    remove_user_from_auction(user, auction)

def send_auction_info(usr: User, auction: Auction):
    msg = {
            "sender": "server",
            "msg_type": "auction_info",
            "content": {
                "auction_id": auction.auction_id,
                "owner": auction.owner.name,
                "item_name": auction.item_name,
                "starting_price": auction.starting_price,
                "bids": [{ "bidder": bid.bidder.name, "amount": bid.amount } for bid in auction.bids],
                "deadline": auction.deadline,
                "open": auction.open,
                "buyer": auction.buyer.name if auction.buyer else None
                }
            }
    usr.conn.sendall(json.dumps(msg).encode("utf-8"))


def add_user_to_auction(usr: User, auction_id: str):
    if not auction_connections.get(auction_id):
        auction_connections[auction_id] = []
    if usr not in auction_connections[auction_id]:
        auction_connections[auction_id].append(usr)

def remove_user_from_auction(usr: User, auction_id):
    if not auction_connections.get(auction_id):
        return
    if usr not in auction_connections[auction_id]:
        return
    auction_connections[auction_id].remove(usr)

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Listening on: ", HOST, PORT)
        while True:
            print("Awaiting new users...")
            conn, addr = s.accept()
            print("Connected: ", addr)
            threading.Thread(target=handle_connection, args=(conn, addr,)).start()


