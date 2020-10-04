# server.py
# Client-Server : Communication

import TxBlock
import Transaction
import Signature
import socket
import pickle

TCP_PORT = 5005
BUFFER_SIZE = 1024

###
###
def newConnect(ip_addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip_addr, TCP_PORT))
    s.listen() 

    return s

###
###
def recvObj(socket):
    conn, addr = socket.accept()
    un_trunc_data = b''
  
    while True:
        data = conn.recv(BUFFER_SIZE)
        
        if not data: 
            break
        
        un_trunc_data = un_trunc_data + data
  
    return pickle.loads(un_trunc_data)


  
if __name__  == "__main__":
    socket = newConnect('localhost')
    newb = recvObj(socket)

    print(newB.data[0])
    print(newB.data[1])

    if newB.is_valid():
        print("Success. Tx is valid.")
    else:
        print("ERRRO. Tx is invalid.")

    if newB.data[0].inputs[0][1] == 2.3:
        print("Success. Input value sent from client matches.")
    else:
        print("ERROR. Wrong input value for block 1, tx 1.")
    if newB.data[0].output[1][1] == 1.1:
        print("Success. Output value sent from client matches.")
    else:
        print("ERROR. Wrong output value for block 1, tx 1.")


    if newB.data[1].inputs[1][1] == 1.0:
        print("Success. Input value sent from client matches.")
    else:
        print("ERROR. Wrong input value for block 1, tx 1.")
    if newB.data[1].output[0][1] == 3.1:
        print("Success. Output value sent from client matches.")
    else:
        print("ERROR. Wrong output value for block 1, tx 1.")

