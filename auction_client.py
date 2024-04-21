import socket
import json
import sys
import uuid
from PyQt5.QtWidgets import QApplication
import auction_client_gui

HOST = "127.0.0.1"
PORT = 8888

class Client:
    def __init__(self):
        self.connected = False
        self.id = uuid.uuid4()
        self.name = None
        self.current_auction = None

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with self.socket:
            self.gui = auction_client_gui.MainMenuWindow(self)
            self.gui.show()
            self.socket.connect((HOST, PORT))
            self.connected = True

    def join_auction(self, auction_id: str):
        if not self.connected:
            return
        if self.current_auction:
            msg = { 
                   "sender": "client",
                   "msg_type": "disconnect_user_from_auction",
                   "content": {
                       "user": {
                           "name": self.name,
                           "id": self.id,
                           },
                       "auction_id": self.current_auction
                       }
                   },
            self.socket.sendall(bytes(json.dumps(msg).encode("utf-8")))

        msg = { 
               "sender": "client",
               "msg_type": "connect_user_to_auction",
               "content": {
                   "user": {
                       "name": self.name,
                       "id": self.id,
                       },
                   "auction_id": auction_id
                   }
               },
        self.socket.sendall(bytes(json.dumps(msg).encode("utf-8")))

    def process_msg(self, msg_bytes: bytes):
        msg = json.loads(msg_bytes.decode("utf-8"))
        if msg["sender"] != "server":
            return
        content = msg["content"]

        if msg["msg_type"] == "auction_info":
            self.gui.set_auction(**content)
            self.current_auction = content["auction_id"]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = Client()
    client.run()
    sys.exit(app.exec_())



