import socket
import threading
import json
import sys
import uuid
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, QObject
import auction_client_gui

HOST = "127.0.0.1"
PORT = 8888

class Client(QObject):
    auction_signal = pyqtSignal(dict)

    def __init__(self):
        super(Client, self).__init__()
        self.connected = False
        self.id = str(uuid.uuid4())
        self.name: str | None = None
        self.current_auction = None

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))
        self.connected = True
        self.gui = auction_client_gui.MainMenuWindow(self)
        self.gui.show()

    def join_auction(self, auction_id: str):
        if not self.connected:
            return
        if self.current_auction:
            self.leave_auction()
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
        self.socket.sendall(json.dumps(msg).encode("utf-8"))
    
    def leave_auction(self):
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
        self.socket.sendall(json.dumps(msg).encode("utf-8"))

    def listen_to_server(self):
        while True:
            print("Waiting to recieve...")
            msg_bytes = self.socket.recv(1024)
            if not msg_bytes:
                break
            print(msg_bytes.decode("utf-8"))
            msg = json.loads(msg_bytes.decode("utf-8"))
            if msg["sender"] != "server":
                return
            content = msg["content"]

            if msg["msg_type"] == "auction_info":
                self.auction_signal.emit(content)
                self.current_auction = content["auction_id"]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = Client()
    client.run()
    threading.Thread(target=client.listen_to_server).start()
    sys.exit(app.exec_())



