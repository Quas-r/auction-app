import json
from typing import Dict, List, Tuple

class User(object):
    def __init__(self, name: str, id: str, address: tuple[str, int]):
        self.name = name
        self.id = id
        self.address = address
    
    def __eq__(self, other: object, /) -> bool:
        if isinstance(other, self.__class__):
            return self.id == other.id
        return False

class AuctionConnectionManager(object):
    def __init__(self):
        self.auction_connections: Dict[str, List[User]] = {}

    def add_user_to_auction(self, usr: User, auction_id: str):
        if not self.auction_connections.get(auction_id):
            self.auction_connections[auction_id] = []
        self.auction_connections[auction_id].append(usr)

    def remove_user_from_auction(self, usr: User, auction_id):
        if not self.auction_connections.get(auction_id):
            return
        # if conn not in self.auction_connections[auction_id]:
        #     return
        self.auction_connections[auction_id].remove(usr)
    
class Bid(object):
    def __init__(self, auction_id: str, bidder: User, amount: float):
        self.auction_id = auction_id
        self.bidder = bidder
        self.amount = amount

class Auction(object):
    def __init__(self, auction_id: str,
                 owner: User,
                 item_name: str,
                 starting_price: float,
                 bids: list[Bid],
                 deadline: None | float,
                 open: bool,
                 buyer: None | User):
        self.auction_id = auction_id
        self.owner = owner
        self.item_name = item_name
        self.starting_price = starting_price
        self.bids = bids
        self.deadline = deadline
        self.open = open
        self.buyer = buyer

def from_json_to_auction(json_string: str) -> Auction:
    auction_dict = json.loads(json_string)
    auction_id = auction_dict["auction_id"]
    owner = User(**auction_dict["owner"])
    item_name = auction_dict["item_name"]
    starting_price = auction_dict["starting_price"]
    bids = []
    for d in auction_dict["bids"]:
        bids.append(Bid(d["auction_id"], User(**d["bidder"]), d["amount"]))
    deadline = auction_dict["deadline"]
    open = auction_dict["open"]
    buyer = None
    if auction_dict["buyer"]:
        buyer = User(**auction_dict["buyer"])
    return Auction(auction_id, owner, item_name, starting_price, bids, deadline, open, buyer)
