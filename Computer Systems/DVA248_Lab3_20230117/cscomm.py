# Module for socket communication for DVA248 Datorsystem
#
#   author: Dag Nystrom, 2023
#

import socket     # For network communication
import pickle     # For serializing/deserializing planet objects

##########################
# SERVER-SIDE FUNCTIONS  #
##########################

def serverInitSocket(ip='127.0.0.1', port=12345):
    '''
    Server-side function to create a socket for new client connections.
        ip:     a string containing the IP address to the server, default is localhost.
        port:   an int containing the port to listen to, default is 12345
    Returns a socket object
    '''
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket to find IP 
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Set/Get options for socket, Allow address reuse 
    serverSocket.bind((ip, port))  # Bind socket to IP and port
    serverSocket.listen()  # Listen for incoming connections
    return serverSocket  # Return the ready server socket

def serverWaitForNewClient(serverSocket: socket):
    '''
    Server-side function that makes the server wait for a new client connecting on the server socket.
        serverSocket:   the socket used for new client connections
    Returns a socket to the new client
    '''
    clientSocket, _ = serverSocket.accept()  # Block until a client connects
    return clientSocket  # Return the socket connected to the client

def serverSendString(clientSocket: socket, mess: str):
    '''
    Server-side function to transmit a string from the server to the client via the client socket
        clientSocket:   the socket to transmit on
        mess:           the message to transmit
    '''
    clientSocket.sendall(mess.encode('utf-8'))  # Encode string to UTF-8 and send
    return  # No return value needed

def serverRecvPlanet(clientSocket: socket):
    '''
    Server-side function to receive a planet object from a client over the client socket.
    The function waits until it receives a planet.
        clientSocket:   the socket to receive from
    Returns the planet object
    '''
    data = b""  # Initialize empty bytes object to store received data
    while True:
        packet = clientSocket.recv(4096)  # Receive up to 4096 bytes
        if not packet:  # If packet is empty, stop receiving
            break
        data += packet  # Append the packet to total data
        try:
            p = pickle.loads(data)  # Try to deserialize data into a planet
            return p  # Return the planet if successful
        except:
            continue  # Keep receiving if data is incomplete
    return  # Return None if no valid object was received

#########################
# CLIENT-SIDE FUNCTIONS #
#########################

def clientInitSocket(ip='127.0.0.1', port=12345):
    '''
    Client-side function to connect to a server via its connecting socket
        ip:     a string containing the IP address to the server, default is localhost
        port:   and integer with the portnumber to use, default is 12345
    Returns a client socket to communicate with the server over
    '''
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create TCP socket to find IP
    try:
        clientSocket.connect((ip, port))  # Connect to the server
    except ConnectionRefusedError:
        print("Could not connect to server")  # Handle connection errors
        exit(1)
    return clientSocket  # Return connected socket

def clientRecvString(clientSocket: socket):
    '''
    Client-side function to receive a string from the server over a socket
        clientSocket:   the socket used for communication with the server
    Returns the string.
    '''
    try:
        data = clientSocket.recv(1024)  # Receive up to 1024 bytes
        return data.decode('utf-8')  # Decode and return the string
    except Exception as e:
        print("Error receiving string from server:", e)  # Log error
        return None  # Return None on failure

def clientSendPlanet(clientSocket: socket, p: object):
    '''
    Client-side function to send a planet object to the server over a socket
        clientSocket:   the socket used for communication with the server
        p:              the planet object to transmit
    '''
    data = pickle.dumps(p)  # Convert object to byte string
    clientSocket.sendall(data)  # Send the serialized data
    return  # No return value