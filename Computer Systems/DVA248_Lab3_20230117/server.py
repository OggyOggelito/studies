#Planet lab in Python for DVA248 Datorsystem
#
#   author: Dag NystrÃ¶m, 2020
#

import threading
import random 
import time
import socket
from space import space
from cscomm import serverInitSocket,serverWaitForNewClient,serverRecvPlanet,serverSendString
from planet import planet
from math import sqrt


SPACEX=800
'''Constant for width of the universe in pixels/coordinates'''
SPACEY=600
'''Constant for height of the universe in pixels/coordinates'''



#class that manages the planet list, it also contains a method for calculating a new position for a planet given all the other.
#DT is the delta-time that specify the increment in time for planet updates. No need to change this.
############## NOTE!!!!! THIS CLASS IS NOT THREAD SAFE AND NEEDS TO BE PROTECTED USING SOME FORM OF MUTEXES
class universe:
    '''
    Class that manages the list of planets in the universe. In the lab you will need to extend this class with your own methods to manage the planets.
    '''
    
        
    planet_list=[]  #The actual list
    DT : int        

    
    def __init__(self, dt=10):
        '''Constructs a universe (i.e. a list of planets), delta time is set to 10 by default which you probably dont need to change. '''
        self.planet_list.clear()
        self.DT=dt
        self.lock = threading.Lock()  # ÄNDRING 1 Mutex lock for thread safety 
        self.draw_list = []           # ÄNDRING 2 Queue for drawing in the graphics thread

    def calculate_planet_pos(self,p:planet):
        '''Method to calculate the position of planet p, relative to all other planets in the system. The method updates the position and age of planet p''' 
        Atotx = 0.0
        Atoty = 0.0
        x = 0.0
        y = 0.0
        r = 0.0
        a = 0.0
        ax = 0.0
        ay = 0.0
        
        G = 6.67259 * pow(10, -11) #Declaration of the gravitational constant
        
        # Lock the universe's shared planet list to ensure thread safety
        with self.lock:
            cur: planet
            for cur in self.planet_list:
                if cur != p:  # Skip self-interaction
                # Calculate the difference in x and y coordinates between current planet and p
                    x = cur.sx - p.sx
                    y = cur.sy - p.sy
                    # Compute the distance between the planets
                    r = sqrt(pow(x, 2) + pow(y, 2))
                    # Gravitational acceleration magnitude from this planet
                    a = G * (cur.mass / pow(r, 2))
                    # Project acceleration into x and y components
                    ay = a * (y / r)
                    ax = a * (x / r)
                    # Accumulate total acceleration from all other planets
                    Atotx += ax
                    Atoty += ay
    
            p.vx = p.vx + (Atotx * self.DT) #Update planet velocity, acceleration and life
            p.vy = p.vy + (Atoty * self.DT)
            p.sx = p.sx + (p.vx * self.DT)
            p.sy = p.sy + (p.vy * self.DT)
            p.life -= 1
    
    # Here you need to extend the planets class with your own methods to manage the planets
    def add_planet(self, p: planet):
        with self.lock:
            self.planet_list.append(p)
    def remove_planet(self, p: planet):
        with self.lock:
            if p in self.planet_list:
                self.planet_list.remove(p)
    def get_planets(self):
        with self.lock:
            return list(self.planet_list)
        
def paint(s: space, u: universe):
    while True:
        time.sleep(0.05)
        with u.lock: # ÄNDRING 4 LÅS I PAINT 
            for sx, sy, rad, color in u.draw_list:
                s.putPlanet(sx, sy, rad, color)
            u.draw_list.clear()
        
def planet_thread(p: planet, u: universe):
    while True:
        time.sleep(0.05)
        u.calculate_planet_pos(p)

        # Set planet color based on name
        if p.name.lower() == "sun":
            color = "yellow"
        elif p.name.lower() == "earth":
            color = "blue"
        elif p.name.lower() == "comet":
            color = "cyan"
        elif p.name.lower() == "oops":
            color = "red"
        else:
            color = "white"

        # Queue draw request in draw_list instead of drawing directly
        with u.lock: # ÄNDRING 5
            u.draw_list.append((p.sx, p.sy, 3, color))

        # Check death cause
        dead = False
        cause = ""
        if p.life <= 0:
            dead = True
            cause = f"Planet {p.name} died from age"
        elif p.sx < 0 or p.sx > SPACEX or p.sy < 0 or p.sy > SPACEY:
            dead = True
            cause = f"Planet {p.name} left the universe"

        if dead:
            u.remove_planet(p)
            clientSock = p.serverGetClientSock()
            if clientSock:
                try:
                    serverSendString(clientSock, cause)
                except:
                    pass
            break
        
def handle_client(clientSock: socket.socket, u: universe):
    while True:
        try:
            p = serverRecvPlanet(clientSock)
            if p is None:
                break
            p.serverAddClientSock(clientSock)
            u.add_planet(p)
            t = threading.Thread(target=planet_thread, args=(p, u), daemon=True)
            t.start()
        except:
            break

def main():
    # Create the universe (i.e, an empty set of planets)
    u=universe()  
    # Create the window on which to draw the universe
    s=space(SPACEX,SPACEY)

    # USER CODE GOES HERE....
    serverSocket = serverInitSocket()
    
    painter = threading.Thread(target=paint, args=(s, u), daemon=True)
    painter.start()

    def accept_loop():
        while True:
            clientSock = serverWaitForNewClient(serverSocket)
            handler = threading.Thread(target=handle_client, args=(clientSock, u), daemon=True)
            handler.start()

    acceptor = threading.Thread(target=accept_loop, daemon=True)
    acceptor.start()
    # Last part of main function is the window management loop, will terminate when window is closed
    s.mainLoop()

if __name__== "__main__":
    main()