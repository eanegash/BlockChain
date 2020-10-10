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
limit_next_char = 255


class TxBlock (CBlock):
    nonce = "AAAAAAA"
    def __init__(self, previousBlock):
        # Reference to Parent class using super functionality
        super(TxBlock, self).__init__([], previousBlock)

    def addTx(self, Tx_in):
        self.data.append(Tx_in)

    def removeTx(self, Tx_in):
        if Tx_in in self.data:
            self.data.remove(Tx_in)
            return True
        return False

    ##
    def check_size(self):
        savePrev = this.previousBlock
        self.previousBlock = None
        this_size = len(pickle.dumps(self))
        self.previousBlock = savePrev

        if this_size > 10000:
            return False
        
        return True

    ## Returns True if total output is greater than total input and 25 WurkiCoin reward.
    def is_valid(self):
        # Reference to Parent Class CBlock.is_valid() method.
        if not super(TxBlock, self).is_valid():
            return False

        spend = {}

        for tx in self.data:
            if not tx.is_valid():
                return False

            for addr,amt,index in tx.inputs:
                if addr in spends:
                    spends[addr] = spends[addr] + amt
                else:
                    spends[addr] = amt
                
                if not index-1 == getLastTxIndex(addr, self.previousBlock):
                    found = False
                    count = 0
                    for tx2 in self.data:
                        for addr2, amt2, indx2 in tx2.inputs:
                            if addr == addr2 and indx2 == index - 1:
                                found=True
                            if addr == addr2 and indx2 == index:
                                count += 1
                    if not found or count > 1:
                        return False

            for addr, amt in tx.outputs:
                if addr in spends:
                    spends[addr] = spends[addr] - amt
                else:
                    spends[addr] = -amt

        for this_addr in spends:
            if spends[this_addr] - getbalance(this_addr, self.previousBlock) > 0.000000001:
                return False

        total_in, total_out = self.count_totals()
        
        # Total Input amount and the 25.0 reward for each additional block must be 
        # less than total output amount. 
        # NOTE: Possibility of floating point error w/ "if total_out > total_in + 25.0
        # NOTE: REFACTOR when transaction amount needs to be less than 1*10^12
        if total_out - total_in - 25.0 > 0.000000000001:
            return False
        if not self.check_size():
            return False
            
        return True

    ##
    ##
    def count_totals(self):
        total_in = 0
        total_out = 0

        for tx in self.data:
        
            for addr, amt, index in tx.inputs:
                total_in = total_in + amt

            for addr, amt in tx.outputs:
                total_out = total_out + amt

        return total_in, total_out

    ### NOTE: Implement a separate Miner Class and Add these methods to it
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
    def find_nonce(self, n=500000):
        for i in range(n):
            self.nonce = ''.join([ chr(random.randint(0, 255)) for i in range(10*leading_zeros)])
        
            if self.valid_nonce():
                return self.nonce

        return None

# Return the longest block in the blockhain. 
def findLongestBlockchain(head_blocks):
    #UPDATE
    longest = -1
    long_head = None

    for b in head_blocks:
        current = b
        this_len = 0

        while current != None:
            this_len += 1
            current = current.previousBlock

        if this_len > longest:
            long_head = b
            longest = this_len

    return long_head

##
def saveBlocks(block_list, filename):
    fp = open(filename, "wb")
    pickle.dump(block_list, fp)
    fp.close()

    return False

##
def loadBlocks(filename):
    fin = open(filename, "rb")
    ret = pickle.load(fin)
    fin.close()
    return ret

##
def getbalance(pu_key, last_block):
    this_block = last_block
    bal = 0.0

    while this_block is not None:
        for tx in this_block.data:
            for addr,amt,index in tx.inputs:
                if addr == pu_key:
                    bal -= amt
            for addr, amt in tx.outputs:
                if addr == pu_key:
                    bal += amt

        this_block = this_block.previousBlock

    return bal

##
##
def getLastTxIndex(pu_key, last_block):
    this_block = last_block
    index = -1

    while this_block is not None:
        for tx in this_block.data:
            for addr,amt,inx in tx.inputs:
                if addr == pu_key and inx > index:
                    index = inx
        # Break loop if index found 
        if index != -1:
            break
        this_block = this_block.previousBlock

    return index



if __name__ == "__main__":
    pr1, pu1 = generate_keys()
    pr2, pu2 = generate_keys()
    pr3, pu3 = generate_keys()

    indeces = {}

    def indexed_input(Tx_inout, public_key, index_map):
        if not public_key in index_map:
            index_map[public_key] = 0
        
        Tx_inout.add_input(public_key, amt, index_map[public_key])
        index_map[public_key] += 1
  

    Tx1 = Tx()
    indexed_input(Tx1, pu1, 1, pu_indeces)
#   Tx1.add_input(pu1, 1)
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

    mine1 = Tx()
    mine1.add_output(pu1, 8.0)
    mine1.add_output(pu2, 8.0)
    mine1.add_output(pu3, 8.0)

    root.addTx(Tx1)
    root.addTx(mine1)

    Tx2 = Tx()
    indexed_input(Tx2, pu2, 1.1, pu_indeces)
#   Tx2.add_input(pu2, 1.1)
    Tx2.add_output(pu3, 1)
    Tx2.sign(pr2)
    root.addTx(Tx2)

    B1 = TxBlock(root)
    Tx3 = Tx()
    indexed_input(Tx3, pu3, 1.1, pu_indeces)
#   Tx3.add_input(pu3, 1.1)
    Tx3.add_output(pu1, 1)
    Tx3.sign(pr3)
    B1.addTx(Tx3)

    Tx4 = Tx()
    indexed_input(Tx4, pu1, 1, pu_indeces)
#   Tx4.add_input(pu2, 1)
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
    indexed_input(Tx5, pu3, 1, pu_indeces)
#   Tx5.add_input(pu3, 1)
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
    B3 = TxBlock(B1)
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

    
    B6 = TxBlock(B4)
    this_pu = pu4
    this_pr = pr4

    for i in range(30):
        newTx = Tx()
        new_pr, new_pu = generate_keys()
        indexed_input(newTx, this_pu, 0.3, pu_indeces)
#        newTx.add_input(this_pu, 0.3)
        newTx.add_output(new_pu, 0.3)
        newTx.sign(this_pr)
        B6.addTx(newTx)

        this_pu = new_pu
        this_pr = new_pr

        savePrev = B6.previousBlock
        B6.previousBlock = None
        this_size = len(pickle.dumps(B6))
        B6.previousBlock = savePrev

        if (B6.is_valid()) and this_size > 10000:
            print("ERROR!! Big Blocks are valid. Size = " + str(this_size))
        elif not B6.is_valid and this_size <= 10000:
            print("ERROR! Small blocks are invalid. Size = " + str(this_size))
        else:
            print("Success! Block size check passed")
    pu_indeces[pu4] = pu_indeces[pu4] - 1


    overspend = Tx()
    indexed_input(overspend, pu1, 45.0, pu_indeces)
#    overspend.add_input(pu1, 45.0)
    overspend.add_output(pu1, 44.5)
    overspend.sign(pr1)
    B7 = TxBlock(B4)
    B7.addTx(overspend)

    if B7.is_valid():
        print("Error! Overspend not detected")
    else:
        print("Success! Overspend detected")


    overspend1 = Tx()
    indexed_input(overspend1, pu1, 5.0, pu_indeces)
#    overspend1.add_input(pu1, 5.0)
    overspend1.add_output(pu1, 4.5)
    overspend1.sign(pr1)

    overspend2 = Tx()
    indexed_input(overspend2, pu1, 15.0, pu_indeces)
#    overspend2.add_input(pu1, 15.0)
    overspend2.add_output(pu3, 14.5)
    overspend2.sign(pr1)

    overspend3 = Tx()
    indexed_input(overspend3, pu1, 5.0, pu_indeces)
#    overspend3.add_input(pu1, 5.0)
    overspend3.add_output(pu4, 4.5)
    overspend3.sign(pr1)

    overspend4 = Tx()
    indexed_input(overspend4, pu1, 8.0, pu_indeces)
#    overspend4.add_input(pu1, 8.0)
    overspend4.add_output(pu2, 4.5)
    overspend4.sign(pr1)

    B8 = TxBlock(B4)
    B8.addTx(overspend1)
    B8.addTx(overspend2)
    B8.addTx(overspend3)
    B8.addTx(overspend4)

    if B8.is_valid():
        print("ERROR! Overspend not detected.")
    else:
        print("Success! Overspend detected.")