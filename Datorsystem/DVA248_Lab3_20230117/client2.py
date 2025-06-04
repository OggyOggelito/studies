import threading
import time
from planet import planet
from cscomm import clientInitSocket, clientRecvString, clientSendPlanet

def receive_messages(sock):
    while True:
        try:
            msg = clientRecvString(sock)
            if msg:
                print("SERVER:", msg)
        except Exception as e:
            print("Error receiving message:", e)
            break

s = clientInitSocket()
threading.Thread(target=receive_messages, args=(s,), daemon=True).start()

# K2 sends only Oops
p = planet("Oops", 500, 400, 0, 0, 1e9, 100)
clientSendPlanet(s, p)

print("K2: Oops sent — waiting for its death notice...")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    s.close()