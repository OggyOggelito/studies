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

# Send Sun, Earth, Comet
p1 = planet("Sun", 300, 300, 0, 0, 1e8, 1e8)
p2 = planet("Earth", 200, 300, 0, 0.008, 1000, 1e8)
p3 = planet("Comet", 500, 300, 0.1, 0, 1000, 1e8)

clientSendPlanet(s, p1)
time.sleep(0.1)
clientSendPlanet(s, p2)
time.sleep(0.1)
clientSendPlanet(s, p3)

print("K1: Sun, Earth, Comet sent — waiting for death notes")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    s.close()