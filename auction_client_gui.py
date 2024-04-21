from auction_client import Client
from PyQt5.QtWidgets import QTextEdit, QLineEdit, QWidget, QVBoxLayout, QPushButton, QListWidget, QMessageBox, QLabel

class AuctionWindow(QWidget):
    def __init__(self, auction_id, owner, item_name, starting_price, bids, deadline, open, buyer):
        super().__init__()
        self.setWindowTitle("Auction")
        self.auction_id = auction_id
        self.owner = owner
        self.item_name = item_name
        self.starting_price = starting_price
        self.bids = bids
        self.deadline = deadline
        self.open = open
        self.buyer = buyer
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.item_label = QLabel("Item Name: " + self.item_name)
        layout.addWidget(self.item_label)

        self.start_price_label = QLabel("Starting Price: $" + str(self.starting_price))
        layout.addWidget(self.start_price_label)

        self.deadline = QLabel("Deadline: " + self.deadline)
        layout.addWidget(self.deadline)

        bids_str = ""
        for bid in self.bids:
            bids_str = bids_str + bid["bidder"] + ": " + str(bid["amount"] + "\n")
        self.bid_history_textedit = QTextEdit(bids_str)
        self.bid_history_textedit.setReadOnly(True)
        layout.addWidget(self.bid_history_textedit)
        
        if self.open:
            self.bid_amount_input = QLineEdit()
            layout.addWidget(self.bid_amount_input)

            self.send_bid_button = QPushButton("Send Bid")
            self.send_bid_button.clicked.connect(self.send_bid)
            layout.addWidget(self.send_bid_button)
        else:
            self.closed_label = QLabel("Auction closed. Buyer: " + self.buyer)
            layout.addWidget(self.closed_label)

        self.setLayout(layout)

    # To-do: Not implemented
    def send_bid(self):
        bid_amount = self.bid_amount_input.text()
        if bid_amount:
            # To-do: Send bid over the network
            QMessageBox.information(self, "Bid Sent", f"Bid of ${bid_amount} sent successfully!")
            self.bid_amount_input.clear()  # Clear the bid amount input after sending the bid
        else:
            QMessageBox.warning(self, "Error", "Please enter a bid amount.")

class MainMenuWindow(QWidget):
    def __init__(self, client: Client):
        super().__init__()
        self.client = client
        self.setWindowTitle("Main Menu")
        self.init_ui()
        self.auction_window = None

    def init_ui(self):
        layout = QVBoxLayout()

        self.auction_list = QListWidget()
        layout.addWidget(self.auction_list)

        start_auction_button = QPushButton("Start Auction")
        start_auction_button.clicked.connect(self.start_auction)
        layout.addWidget(start_auction_button)

        join_auction_button = QPushButton("Join Auction")
        join_auction_button.clicked.connect(self.join_auction)
        layout.addWidget(join_auction_button)

        self.setLayout(layout)

        # To-do: Change this
        self.auctions = {"Auction 1": "3ab496a1-e504-457d-9598-a97209105a19", "Auction 2": "59d6fafb-0a53-4805-b1da-19cbaefc4236"}

        for auction_id in self.auctions:
            self.auction_list.addItem(auction_id)

    # To-do: Not implemented
    def start_auction(self):
        # Placeholder for starting an auction
        QMessageBox.information(self, "Start Auction", "Placeholder for starting an auction")

    def join_auction(self):
        selected_item = self.auction_list.currentItem()
        if selected_item:
            auction_name = selected_item.text()
            auction_id = self.auctions.get(auction_name)
            if auction_id:
                self.client.join_auction(auction_id)
        else:
            QMessageBox.warning(self, "Error", "No auction selected. Please select an auction to join.")

    def set_auction(self, auction_id, owner, item_name, starting_price, bids, deadline, open, buyer):
        self.auction_window = AuctionWindow(auction_id, owner, item_name, starting_price, bids, deadline, open, buyer)
        self.auction_window.show()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     main_menu = MainMenuWindow()
#     main_menu.show()
#     sys.exit(app.exec_())

