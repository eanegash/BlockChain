# SocketUtils.py
# Socket Communication Utility

import socket
import pickle
import select


TCP_PORT = 5005
BUFFER_SIZE = 1024

###
###
def newServerConnect(ip_addr, port=TCP_PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip_addr, port))
    s.listen() 

    return s

###
###
def recvObj(socket):
    
    inputs, outputs, errs = select.select([socket], [], [socket], 8)
    
    if socket in inputs:
    
        conn, addr = socket.accept()
        un_trunc_data = b''
  
        while True:
            data = conn.recv(BUFFER_SIZE)
        
            if not data: 
                break
        
            un_trunc_data = un_trunc_data + data
  
        return pickle.loads(un_trunc_data)

    return None

###
###
def sendBlock(ip_addr, blk, port=TCP_PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip_addr, port))

    data = pickle.dumps(blk)
    s.send(data)
    
    s.close()

    return False



if __name__ == "__main__":
    # Test return w/o blocking
    server = newServerConnect('localhost')
    o = recvObj(server)
    
    print(o)
    print("Success!")

    server.close()