# WurkiCoin

import threading
import time
import Wallet
import Miner
import Signature

wallets = []
miners = []
my_ip = 'localhost'
wallets.append((my_ip, 5006))
miners.append((my_ip, 5005))

tMS = None
tNF = None

tWS = None

def startMiner():
    global tMS, tNF
    
    # Load public_key
    try:
        my_pu = Signature.loadPublic("public.key")
    except:
        print("No public.key, need to generate?")
        pass

    # Start nonceFinder
    # Start minerServer
    tMS = threading.Thread(target=Miner.minerServer, args=((my_ip, 5005),))
    tNF = threading.Thread(target=Miner.nonceFinder, args=(wallets, my_pu))
    tMS.start()
    tNF.start()

    return True

def startWallet():
    global tWS 

    # Load public and private keys
    Wallet.my_private, Wallet.my_public = Signature.loadKeys(("private.key", "public.key")) 

    # Start WalletServer
    tWS = threading.Thread(target=Wallet.walletServer, args=((my_ip, 5006),))
    tWS.start()

    return True


def stopMiner():
    global tMS, tNF

    # Stop nonceFinder
    # Stop minerServer
    Miner.StopAll()
    if tMS: tMS.join()
    if tNF: tNF.join()

    tMS = None
    tNF = None

    return True

def stopWallet():
    global tWS
    # Stop WalletServer
    Wallet.StopAll()
    if tWS: tWS.join()
    tWS = None
    # Save head_blocks
    return True


def getBalance(pu_key):
    if not tWS:
        print("Start the server. Call startWallet before checking balance(s)")
        return 0.0

    return Wallet.getbalance(pu_key)

def sendCoin(pu_rect, amt, tx_fee):
    Wallet.sendCoins(Wallet.my_public, amt+tx_fee, Wallet.my_private, pu_recv, amt, miners)
    return True


def makeNewKeys():
    return None, None



if __name__ == "__main__":
    startMiner()
    startWallet()

    other_public = ''

    time.sleep(2)

    print(getBalance(Wallet.my_public))
    
    sendCoin( other_public, 1.0, 0.001)
    time.sleep(20)

    print(getBalance(other_public))
    print(getBalance(my_public))

    time.sleep(1)
    stopWallet()
    stopMiner()