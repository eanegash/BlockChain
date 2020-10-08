# Miner


import SocketUtils
import TxBlock
import Transaction
import pickle


# Currently designed with 'Full Wallet' implementation

wallets = [('localhost', 5005)]
tx_list = []
head_blocks = [None]
break_now = False


def StopAll():
    break_now = True


## Miner computes new Nonce and sets Block to the top of the BlockChain.
# Returns BlockChain to everyone in the wallet list.
# IP_ADDR - 
# WALLET_LIST -
# MY_PUBLIC - 
def minerServer(my_addr):
    global tx_list
    global break_now
    
    # Load tx_list
    try:
        tx_list = loadTxList("Txs.dat")
    except:
        print("No previous Txs. Starting fresh.")
        tx_list = []

    my_ip, my_port = my_addr
    # Open Server Connection
    server = SocketUtils.newServerConnect(my_ip, my_port)

    # Receive transactions from wallet
    while not break_now:
        newTx = SocketUtils.recvObj(server)

        # isinstance requests if an Object is an Instance of a Class. 
        if isinstance(newTx, Transaction.Tx):
            tx_list.append(newTx)

    saveTxList(tx_list, "Txs.dat")

    return False

##
def nonceFinder(wallet_list, miner_public):
    global break_now

    # Load head_blocks
    try:
        head_blocks = TxBlock.loadBlocks("AllBlocks.dat")
    except:
        print("MINER: No previous blocks found. Starting fresh.")
        head_blocks = [None]

    # Collect transactions into a block
    while not break_now:
        newBlock = TxBlock.TxBlock(TxBlock.findLongestBlockchain(head_blocks)) 

        # Placeholder transaction, that stores an output transaction.
        placeholder = Transaction.Tx()
        placeholder.add_output(miner_public, 25.0)
        newBlock.addTx(placeholder)

        #TODO Sort tx_list by tx fee per byte. In 10000 byte want to cram in as many transactions fees we can.
        for tx in tx_list:
            newBlock.addTx(tx)
            # Transaction is too big remove it.
            if not newBlock.check_size():
                newBlock.removeTx(tx)
                break
 
        newBlock.removeTx(placeholder)

        # Compute and collect Miner's reward
        total_in, total_out = newBlock.count_totals()
        miner_reward = Transaction.Tx()
        miner_reward.add_output(miner_public, 25.0+total_in-total_out)
        newBlock.addTx(miner_reward)

        # Find the Nonce
        print("Finding Nonce...")
        newBlock.find_nonce(5000)
        if newBlock.valid_nonce():
            print("Success! Good nonce found.")

            # Replace the previously longest head in the set of blocks
            head_blocks.remove(newBlock.previousBlock)
            head_blocks.append(newBlock)

            # Send block to everyone in the wallet_list. Wallet will package block.
            savePrev = newBlock.previousBlock
            newBlock.previousBlock = None
            for ip_addr, port in wallet_list:
                SocketUtils.sendObj(ip_addr, newBlock, 5006)
            newBlock.previousBlock = savePrev

            # Remove used transactions from tx_list
            for tx in newBlock.data:
                if tx != miner_reward:
                    tx_list.remove(tx)

    # Save head-_blocks
    TxBlock.saveBlocks(head_blocks, "AllBlocks.dat")

    return True

##
def loadTxList(filename):
    fin = open(filename, "rb")
    ret = pickle.load(fin)
    fin.close()

    return ret

##
def saveTxList(the_list, filename):
    fp = open(filename, "wb")
    pickle.dump(the_list, fp)
    fp.close

    return True



if __name__ == "__main__":
    import threading
    import time
    import Signature

    my_pr, my_pu = Signature.generate_keys()
    # args need to be passed as a TUPLE.
    t1 = threading.Thread(target=minerServer, args=(('localhost', 5005),))
    t2 = threading.Thread(target=nonceFinder, args=(wallets, my_pu))
    
    server = SocketUtils.newServerConnect('localhost', 5006)

    t1.start()
    t2.start()

    pr1, pu1 = Signature.generate_keys()
    pr2, pu2 = Signature.generate_keys()
    pr3, pu3 = Signature.generate_keys()

    Tx1 = Transaction.Tx()
    Tx2 = Transaction.Tx()

    Tx1.add_input(pu1, 4.0)
    Tx1.add_input(pu2, 1.0)
    Tx1.add_output(pu3, 4.8)    
    Tx2.add_input(pu3, 4.0)
    Tx2.add_output(pu2, 4.0)

    Tx2.add_reqd(pu1)

    Tx1.sign(pr1)
    Tx1.sign(pr2)
    Tx2.sign(pr3)
    Tx2.sign(pr1)

    new_tx_list = [Tx1, Tx2]
    saveTxList(new_tx_list, "Txs.dat")
    new_new_tx_list = loadTxList("Txs.dat")

    print(Tx1.is_valid())
    print(Tx2.is_valid())

    for tx in new_new_tx_list:
       try:
            SocketUtils.sendBlock('localhost',Tx1)
            print("Tx1 Sent")
            SocketUtils.sendBlock('localhost',Tx2)
            print("Tx2 Sent")
        except:
            print("ERROR. Unsuccessful connection.")
    
    for i in range(30):
        newBlock = SocketUtils.recvObj(server)
        if newBlock:
            break
    
    if newBlock.is_valid():
        print("Success! Block is valid.")
    if newBlock.valid_nonce():
        print("Success! Nonce is valid.")
    
    for i in newBlock.data:
        try:
            if tx.inputs[0][0] == pu1 and tx.inputs[0][1] == 4.0:
                print("Tx1 is present.")
        except:
            pass
        try:
            if tx.inputs[0][0] == pu3 and tx.inputs[0][1] == 4.0:
                print("Tx2 is present")
        except:
            pass

    time.sleep(20)
    StopAll()
    time.sleep(2)

    server.close()

    t1.join()
    t2.join()


    print('DONE!')