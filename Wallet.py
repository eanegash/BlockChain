# Wallet


import SocketUtils
import Signature
import Transaction

head_blocks = [None]

# Currently designed with 'Full Wallet' implementation

pr1, pu1 = Signature.generate_keys()
pr2, pu2 = Signature.generate_keys()
pr3, pu3 = Signature.generate_keys()

Tx1 = Transaction.Tx()
Tx2 = Transaction.Tx()

Tx1.add_input(pu1, 4.0)
Tx1.add_input(pu2, 1.0)
Tx2.add_input(pu3, 4.0)

Tx1.add_output(pu3, 4.8)
Tx2.add_output(pu2, 4.0)

Tx2.add_reqd(pu1)

Tx1.sign(pr1)
Tx1.sign(pr2)
Tx2.sign(pr3)
Tx2.sign(pr1)

try:
    SocketUtils.sendBlock('localhost',Tx1)
    SocketUtils.sendBlock('localhost',Tx2)
except:
    print("ERROR. Unsuccessful connection attempt.")

server = SocketUtils.newServerConnect('localhost', 5006)

for i in range(10):
    newBlock = SocketUtils.recvObj(server)
    if newBlock:
        break

server.close()

if newBlock.is_valid():
    print("Success! Block is valid.")
if newBlock.valid_nonce():
    print("Success! Nonce is valid.")

for i in newBlock.data:
    try:
        if tx.inputs[0][0] == pu1 and tx.inputs[0][1] == 4.0:
            print("Tx1 is present.")
    try:
        if tx.inputs[0][0] == pu3 and tx.inputs[0][1] = 4.0:
            print("Tx2 is present")

            
    
for b in head_blocks:
    if newBlock.previousHash == b.computeHash():
        newBlock.previousBlock = b
        head_blocks.remove(b)
        head_blocks.append(newBlock)