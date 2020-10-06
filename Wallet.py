# Wallet

import time
import SocketUtils
import Signature
import Transaction
import Miner
import threading
import TxBlock


break_now = False
head_blocks = [None]
wallets  = [('localhost', 5006)]
miners = [('localhost', 5000)]


##
def walletServer(my_addr):
    server = SocketUtils.newServerConnect('localhost', 5006)

    while not break_now
        newBlock = SocketUtils.recvObj(server)
        if isinstance(newBlock, TxBlock.TxBlock):
            print("Rec'd block")
            for b in head_blocks:
                if b == None:
                    if newBlock.previousHash == None:
                        newBlock.previousBlock = b
                        head_blocks.remove(b)
                        head_blocks.append(newBlock)
                        print("Added to head_block")
                if newBlock.previousHash == b.computeHash():
                    newBlock.previousBlock = b
                    head_blocks.remove(b)
                    head_blocks.append(newBlock)
                    print("Added to head_block")    
    
                #TODO Add to an non-head block.
    server.close()  

    return True

##
def getbalance(pu_key):
    return 0.0

##
def sendCoins(pu_send, amt_send, pr_send, pu_recv, amt_recv, miners_list_addr):
    return True




if __name__ == "__main__":
    miner_pr, miner_pu = Signature.generate_keys()
    # Need args to be passed a TUPLE.
    t1 = threading.Thread(target=Miner.minerServer, args=(('localhost', 5005),))
    t2 = threading.Thread(target=Miner.nonceFinder, args=(wallets, miner_pu))
    t3 = threading.Thread(target=walletServer, args=(('localhost', 5006),))

    t1.start()
    t2.start()
    t3.start()

    pr1, pu1 = Signature.generate_keys()
    pr2, pu2 = Signature.generate_keys()
    pr3, pu3 = Signature.generate_keys()

    #
    bal1 = getbalance(pu1)
    bal2 = getbalance(pu1)
    bal3 = getbalance(pu1)

    #
    sendCoins(pu1, 1.0, pr1, pu2, 1.0, miners)
    sendCoins(pu1, 1.0, pr1, pu3, 0.3, miners)

    time.sleep(30)

    #
    new1 = getbalance(pu1)
    new2 = getbalance(pu1)
    new3 = getbalance(pu1)

    #
    if abs(new1 - bal1 + 1.3) > 0.00000001:
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

    Miner.break_now = True
    break_now = True
    t1.join()
    t2.join()
    t3.join()