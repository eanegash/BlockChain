# Miner

import SocketUtils
import TxBlock
import Transaction
import Signature


# Currently designed with 'Full Wallet' implementation

wallets = ['localhost']
tx_list = []
head_blocks = [None]

# Return the longest block in the blockhain. 
def findLongestBlockchain():
    #UPDATE
    longest = -1
    long_head = None

    for b in head_blocks():
        current = b
        this_len = 0

        while current != None:
            this_len += 1
            current = current.previousBlock

        if this_len > longest:
            long_head = b
            longest = this_len

    return long_head


# Miner computes new Nonce and sets Block to the top of the BlockChain.
# Returns BlockChain to everyone in the wallet list.
# IP_ADDR - 
# WALLET_LIST -
# MY_PUBLIC - 
def minerServer(ip_addr, wallet_list, my_public):

    # Open Server Connection
    server = SocketUtils.newServerConnect('localhost')

    # Receive 2 transactions
    for i in range(10):
        newTx = SocketUtils.recvObj(server)

        # isinstance requests if an Object is an Instance of a Class. 
        if isinstance(newTx, Transaction.Tx):
            tx_list.append(newTx)

        if len(tx_list) >= 2:
            break
    
    # Collect transactions into a block
    newBlock = TxBlock.TxBlock(findLongestBlockchain()) 
    newBlock.addTx(tx_list[0])
    newBlock.addTx(tx_list[1])
 
    # Compute and collect Miner's reward
    total_in, total_out = newBlock.count_totals()
    miner_reward = Transaction.Tx()
    miner_reward.add_output(my_public, 25.0+total_in-total_out)
    newBlock.addTx(miner_reward)

    # Find the Nonce
    newBlock.find_nonce()
    for i in range(10):
        newBlock.find_nonce()
        if newBlock.valid_nonce():
            break

    if not newBlock.valid_nonce():
        print("ERROR. Couldn't locate Nonce.")
        return False

    # Send block to everyone in the wallet_list
    for ip_addr in wallet_list:
        SocketUtils.sendObj(ip_addr, newBlock, 5006)

    # Replace the previously longest head in the set of blocks
    head_blocks.remove(newBlock.previousBlock)
    head_blocks.append(newBlock)

    return False


my_pr, my_pu = Signature.generate_keys()
minerServer('localhost', wallets, my_pu)