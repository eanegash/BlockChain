# Wallet


import SocketUtils
import Transaction
import TxBlock
import pickle
import Signature


break_now = False
head_blocks = [None]
wallets  = [('localhost', 5006)]
miners = [('localhost', 5000)]

my_private, my_public = Signature.generate_keys()

def StopAll():
    break_now = True

##
def walletServer(my_addr):
    global head_blocks
    
    # Load head_blocks
    try:
        # Save Wallet blocks to different file to Miner: AllBlocks.dat. 
        # Otherwise dangerous to read at the same time if you were writing to the same file.
        head_blocks = TxBlock.loadBlocks("WalletBlocks.dat")
    except:
        print("WS: No previous blocks found. Starting fresh.")
        head_blocks = [None]
    
    server = SocketUtils.newServerConnect('localhost', 5006)

    while not break_now:
        newBlock = SocketUtils.recvObj(server)
        if isinstance(newBlock, TxBlock.TxBlock):
            print("Rec'd block")
            for b in head_blocks:
                if b == None:
                    if newBlock.previousHash == None:
                        newBlock.previousBlock = b
                        if not newBlock.is_valid():
                            print("Nonce isn't valid.")
                        else:
                            head_blocks.remove(b)
                            head_blocks.append(newBlock)
                            print("Added to head_block")
                elif newBlock.previousHash == b.computeHash():
                    newBlock.previousBlock = b
                    if not newBlock.is_valid():
                        print("Nonce isn't valid.")
                    else:                    
                        head_blocks.remove(b)
                        head_blocks.append(newBlock)
                        print("Added to head_block")    
    
                #TODO Add to an non-head block.
    
    # Save head_block
    TxBlock.saveBlocks(head_blocks, "WalletBlocks.dat")

    server.close()  

    return True

##
def getbalance(pu_key):
    long_chain = TxBlock.findLongestBlockchain(head_blocks)
    this_block = long_chain
    bal = 0.0

    while this_block is not None:
        for tx in this_block.data:
            for addr, amt in tx.inputs:
                if addr == pu_key:
                    bal -= amt
            for addr, amt in tx.outputs:
                if addr == pu_key:
                    bal += amt

        this_block = this_block.previousBlock

    return bal


##
def sendCoins(pu_send, amt_send, pr_send, pu_recv, amt_recv, miners_list_addr):
    newTx = Transaction.Tx()
    newTx.add_input(pu_send, amt_send)
    newTx.add_output(pu_recv, amt_recv)
    newTx.sign(pr_send)
    SocketUtils.sendBlock('localhost',newTx)
    return True


##
def loadKeys(pr_file, pu_file):
    return Signature.loadPrivate(pr_file), Signature.loadPublic(pu_file)




if __name__ == "__main__":
    import Signature
    import Miner
    import threading
    import time

    miner_pr, miner_pu = Signature.generate_keys()
    # Need args to be passed a TUPLE.
    t1 = threading.Thread(target=Miner.minerServer, args=(('localhost', 5005),))
    t2 = threading.Thread(target=Miner.nonceFinder, args=(wallets, miner_pu))
    t3 = threading.Thread(target=walletServer, args=(('localhost', 5006),))

    t1.start()
    t2.start()
    t3.start()

    pr1, pu1 = loadKeys("private.key", "public.key")
    pr2, pu2 = Signature.generate_keys()
    pr3, pu3 = Signature.generate_keys()

    # Gather Balance
    bal1 = getbalance(pu1)
    bal2 = getbalance(pu1)
    bal3 = getbalance(pu1)

    # Send Coins
    sendCoins(pu1, 0.1, pr1, pu2, 0.1, miners)
    sendCoins(pu1, 0.1, pr1, pu2, 0.1, miners)
    sendCoins(pu1, 0.1, pr1, pu2, 0.1, miners)
    sendCoins(pu1, 0.1, pr1, pu2, 0.1, miners)
    sendCoins(pu1, 0.1, pr1, pu2, 0.1, miners)
    sendCoins(pu1, 0.1, pr1, pu2, 0.1, miners)
    sendCoins(pu1, 0.1, pr1, pu2, 0.1, miners)
    sendCoins(pu1, 0.1, pr1, pu2, 0.1, miners)
    sendCoins(pu1, 0.1, pr1, pu2, 0.1, miners)
    sendCoins(pu1, 0.1, pr1, pu2, 0.1, miners)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03, miners)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03, miners)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03, miners)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03, miners)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03, miners)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03, miners)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03, miners)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03, miners)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03, miners)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03, miners)

    time.sleep(120)

    # Load (Save) all blocks
    TxBlock.saveBlocks(head_blocks, "AllBlocks.dat")
    head_blocks = TxBlock.loadBlocks("AlBlocks.dat")

    # Gather Balance
    new1 = getbalance(pu1)
    new2 = getbalance(pu1)
    new3 = getbalance(pu1)

    #
    if abs(new1 - bal1 + 2.0) > 0.00000001:
        print("Error! Wrong balance for pu1")
    else:
        print('Success. Balance is correct for pu1')

    if abs(new2 - bal2 - 1.0) > 0.00000001:
        print("Error! Wrong balance for pu2")
    else:
        print('Success. Balance is correct for pu2')

    if abs(new3 - bal3 - 0.3) > 0.00000001:
        print("Error! Wrong balance for pu3")
    else:
        print('Success. Balance is correct for pu3')

    Miner.StopAll
    StopAll()
    t1.join()
    t2.join()
    t3.join()