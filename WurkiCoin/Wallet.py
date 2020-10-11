# Wallet


import SocketUtils
import Transaction
import TxBlock
import pickle
import Signature


break_now = False
head_blocks = [None]
wallets  = [('localhost', 5006)]
miners = [('localhost', 5005)]
#miners = [('localhost', 5005), ('localhost', 5007)]
#Transaction Index
tx_index = {}

my_private, my_public = Signature.generate_keys()

def StopAll():
    break_now = True

##
def walletServer(my_addr):
    global head_blocks
    global tx_index
    
    # Load head_blocks
    try:
        # Save Wallet blocks to different file to Miner: AllBlocks.dat. 
        # Otherwise dangerous to read at the same time if you were writing to the same file.
        head_blocks = TxBlock.loadBlocks("AllBlocks.dat")
    except:
        print("No previous blocks found. Starting fresh.")
        head_blocks = [None] #TxBlock.loadBlocks("Genesis.dat")

    try:
        fp = open("tx_index", "rb")
        tx_index = pickle.load(fp)
        fp.close()
    except:
        tx_index = {}
    
    server = SocketUtils.newServerConnect('localhost', 5006)

    while not break_now:
        newBlock = SocketUtils.recvObj(server)
        if isinstance(newBlock, TxBlock.TxBlock):
            TxBlock.processNewBlock(newBlock, head_blocks)
        #TODO handle orphaned blocks. What is Child appears before the parent block?
    
    server.close()
    # Save head_block
    TxBlock.saveBlocks(head_blocks, "WalletBlocks.dat")

    fp = open("tx_index.dat", "wb")
    pickle.dump(tx_index, fp)
    fp.close()  

    return True


##
def getbalance(pu_key):
    long_chain = TxBlock.findLongestBlockchain(head_blocks)
    
    return TxBlock.getbalance(pu_key, long_chain)

##
def sendCoins(pu_send, amt_send, pr_send, pu_recv, amt_recv):
    newTx = Transaction.Tx()
    if not pu_send in tx_index:
        tx_index[pu_send] = 0
    newTx.add_input(pu_send, amt_send, tx_index[pu_send])
    newTx.add_output(pu_recv, amt_recv)
    newTx.sign(pr_send)
    
    for ip, port in miners:
        SocketUtils.sendBlock(ip,newTx,port)
    tx_index[pu_send] += 1
    
    return True


##
def loadKeys(pr_file, pu_file):
    return Signature.loadPrivate(pr_file), Signature.loadPublic(pu_file)




if __name__ == "__main__":
    import Signature
    import Miner
    import threading
    import time

    ## Duplicate Transactions. Testing 
    def Thief(my_addr):
        my_ip, my_port = my_addr
        # Open Server Connection.
        server = SocketUtils.newServerConnect(my_ip, my_port)

        # Receive transactions from wallet.
        while not break_now:
            newTx = SocketUtils.recvObj(server)

            # isinstance requests if an Object is an Instance of a Class. 
            if isinstance(newTx, Transaction.Tx):
                # Open up to each of the miners and send a SECOND transaction.
                for ip, port in miners:
                    #Break Infinite Loop. Where Thief sends transactions to him/her-self.
                    if not (ip==my_ip and port == my_port):
                        SocketUtils.sendBlock(ip, newTx, port)


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
    sendCoins(pu1, 0.1, pr1, pu2, 0.1)
    sendCoins(pu1, 0.1, pr1, pu2, 0.1)
    sendCoins(pu1, 0.1, pr1, pu2, 0.1)
    sendCoins(pu1, 0.1, pr1, pu2, 0.1)
    sendCoins(pu1, 0.1, pr1, pu2, 0.1)
    sendCoins(pu1, 0.1, pr1, pu2, 0.1)
    sendCoins(pu1, 0.1, pr1, pu2, 0.1)
    sendCoins(pu1, 0.1, pr1, pu2, 0.1)
    sendCoins(pu1, 0.1, pr1, pu2, 0.1)
    sendCoins(pu1, 0.1, pr1, pu2, 0.1)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03)

    time.sleep(120)

    # Load (Save) all blocks
    TxBlock.saveBlocks(head_blocks, "AllBlocks.dat")
    head_blocks = TxBlock.loadBlocks("AlBlocks.dat")

    # Gather Balance
    new1 = getbalance(pu1)
    new2 = getbalance(pu1)
    new3 = getbalance(pu1)

    # Verify Balances
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


    # Thief will try to duplicate transactions
    # Args is a Tuple of one element. That element stores localhost and ip.
    miner.append(('localhost', 5007))
    t4 = threading.Thread(target=Thief,args=(('localhost', 5007),))
    t4.start()
    sendCoins(pu2, 0.2, pr2, pu1, 0.2)
    time.sleep(20)

    # Check Balances
    newnew1 = getBalance(pu1)
    if (abs(newnew1 - new1 -0.2)) > 0.000000001:
        print("ERROR! Duplicate Txs accepted.")
    else:
        print("Success! Duplicate Txs are rejected.")

    Miner.StopAll()

    num_heads = len(head_blocks)
    sister = TxBlock.TxBlock(head_blocks[0].previousBlock.previousBlock)
    sister.previousBlock = None
    SocketUtils.sendBlock('localhost', sister, 5006)

    time.sleep(10)

    if (len(head_blocks) == num_heads + 1):
        print("Success! New head_block created.")
    else:
        print("ERROR@ Failed to add sister block.")

    StopAll()
    t1.join()
    t2.join()
    t3.join()