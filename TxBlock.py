# TxBlock.py

import time
import pickle
import random
from BlockChain import CBlock
from Transaction import Tx
from Signature import generate_keys, sign, verify
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


leading_zeros = 2
limit_next_char = 25


class TxBlock (CBlock):
    nonce = "AAAAAAA"
    def __init__(self, previousBlock):
        # Reference to Parent class using super functionality
        super(TxBlock, self).__init__([], previousBlock)

    def addTx(self, Tx_in):
        self.data.append(Tx_in)

    def is_valid(self):
        if not super(TxBlock, self).is_valid():
            return False

        total_in, total_out = self.__count_totals()
        
        # Total Input amount and the 25.0 reward for each additional block must be 
        # less than total output amount. 
        # NOTE: Possibility of floating point error w/ "if total_out > total_in + 25.0
        # NOTE: REFACTOR when transaction amount needs to be less than 1*10^12
        if total_out - total_in - 25.0 > 0.000000000001:
            return False
        
        return True

    # Internal Private Function. To calculate the total transaction Input and Outputs amounts.
    def __count_totals(self):
        total_in = 0
        total_out = 0

        for tx in self.data:
        
            for addr, amt in tx.inputs:
                total_in = total_in + amt

            for addr, amt in tx.outputs:
                total_out = total_out + amt

        return total_in, total_out

    ### NOTE: Implementat a separate Miner Class and Add these methods to it
    ## Returns a Boolean. 
    ## Determines the Nonce's validity. 
    def valid_nonce(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data), 'utf-8'))
        digest.update(bytes(str(self.previousHash), 'utf-8'))
        digest.update(bytes(str(self.nonce), 'utf-8'))

        this_hash =  digest.finalize()

        if this_hash[:leading_zeros] != ''.join(["\x00" for i in range(leading_zeros)]): 
            return False
        
        return int(this_hash[leading_zeros]) < limit_next_char

    ## Returns Nonce or None. Once Nonce is determined to be valid or not. 
    def find_nonce(self):
        for i in range(500000):
            self.nonce = ''.join([ chr(random.randint(0, 255)) for i in range(10*leading_zeros)])
        
            if self.valid_nonce():
                return self.nonce

        return None



if __name__ == "__main__":
    pr1, pu1 = generate_keys()
    pr2, pu2 = generate_keys()
    pr3, pu3 = generate_keys()

    Tx1 = Tx()
    Tx1.add_input(pu1, 1)
    Tx1.add_output(pu2, 1)
    Tx1.sign(pr1)

    if Tx1.is_valid():
        print("Success! Tx is  valid")

    savefile = open("tx.dat", "wb")
    pickle.dump(Tx1, savefile)
    savefile.close()

    loadfile = open("tx.dat", "rb")
    newTx = pickle.load(loadfile)

    if newTx.is_valid():
        print("Success! Loaded tx is valid!")
    loadfile.close()

    root = TxBlock(None)
    root.addTx(Tx1)

    Tx2 = Tx()
    Tx2.add_input(pu2, 1.1)
    Tx2.add_output(pu3, 1)
    Tx2.sign(pr2)
    root.addTx(Tx2)

    B1 = TxBlock(root)
    Tx3 = Tx()
    Tx3.add_input(pu3, 1.1)
    Tx3.add_output(pu1, 1)
    Tx3.sign(pr3)
    B1.addTx(Tx3)

    Tx4 = Tx()
    Tx4.add_input(pu1, 1)
    Tx4.add_output(pu2, 1)
    Tx4.add_reqd(pu3)
    Tx4.sign(pr1)
    Tx4.sign(pr3)
    B1.addTx(Tx4)
    # Testing Nonce
    start = time.time() # Grab time from CPU clock
    print(B1.find_nonce())
    elapsed_time = time.time() - start 
    print("Elapsed time: " + str(elapsed_time) + " sec.")
    if elapsed_time < 60:
        print("ERROR: Mining is too fast " + str(elapsed_time) + " sec. < 60 sec." )
    if B1.valid_nonce():
        print("Success! Nonce is good")
    else:
        print("ERROR: Bad Nonce")

    savefile = open("block.dat", "wb")
    pickle.dump(B1, savefile)
    savefile.close()

    loadfile = open("block.dat", "rb")
    load_B1 = pickle.load(loadfile)

    load_B1.is_valid()

    for b in [root, B1, load_B1, load_B1.previousBlock]:
        if b.is_valid():
            print("Success! Valid block.")
        else:
            print("ERROR! Bad Block")

    if B1.valid_nonce():
        print("Success! Nonce is good after save and load.")
    else:
        print("ERROR: Bad Nonce after load.")

    B2 = TxBlock(B1)
    Tx5 = Tx()
    Tx5.add_input(pu3, 1)
    Tx5.add_output(pu1, 100)
    Tx5.sign(pr3)
    B2.addTx(Tx5)

    load_B1.previousBlock.addTx(Tx4)
    for b in [B2, load_B1]:
        if b.is_valid():
            print("ERROR! Bad block verified.")
        else:
            print("Success! Bad blocks detected.")

    loadfile.close()

    # Testing Mining Rewards
    pr4, pu4 = generate_keys()
    B3 = TxBlock(B2)
    B3.addTx(Tx2)
    B3.addTx(Tx3)
    B3.addTx(Tx4)
    Tx6 = Tx()
    Tx6.add_output(pu4, 25) # Block creation reward of 25
    B3.addTx(Tx6)

    if B3.is_valid():
        print("Success! Block reward succeeds.")
    else:
        print("ERROR! Block reward fail.")

    # Testing Transaction Fee + Reward
    B4 = TxBlock(B3)
    B4.addTx(Tx2)
    B4.addTx(Tx3)
    B4.addTx(Tx4)
    Tx7 = Tx()
    Tx7.add_output(pu4, 25.2) # Block creation reward of 25 plus 0.2 Transaction Fee
    B4.addTx(Tx7)

    if B4.is_valid():
        print("Success! Tx fees succeeded.")
    else:
        print("ERROR! Tx fees Failed.")

    # Testing Greedy Miner
    B5 = TxBlock(B4)
    B5.addTx(Tx2)
    B5.addTx(Tx3)
    B5.addTx(Tx4)
    Tx8 = Tx()
    Tx8.add_output(pu4, 26.2)
    B5.addTx(Tx8)

    if not B5.is_valid():
        print("Success! Greedy miner detected.")
    else:
        print("ERROR! Greedy miner not detected.")