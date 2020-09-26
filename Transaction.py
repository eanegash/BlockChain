# Transaction.py

import Signature
#Signatures.sign
#Signatures.verify

class Tx:
    inputs = None
    outputs = None
    sigs = None
    reqd = None

    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.sigs = []
        self.reqd = []

    def add_input(self, from_addr, amount):
        # Tuple: inputs will represent a list of tuples representing addr(string) & amounts(float)
        self.inputs.append((from_addr, amount))

    def add_output(self, to_addr, amount):
        self.output.append((to_addr, amount))

    def add_reqd(self, addr):
        self.reqd.append(addr)

    def sign(self, private):
        ### ADD CODE HERE ###
        Signature.sign(message, private)

    def is_valid(self):
        ### ADD CODE HERE ###
        Signature.verify(message, sig, public)


# Testing
if __name__ == "__main__":
    pr1, pul1 = Signature.generate_keys()
    pr2, pul2 = Signature.generate_keys()
    pr3, pul3 = Signature.generate_keys()
    pr4, pul4 = Signature.generate_keys()

    # Correct Transactions
    Tx1 = Tx()
    Tx1.add_input(pul1, 1)
    Tx1.add_output(pul2, 1)
    Tx1.sign(pr1)

    Tx2 = Tx()
    Tx2.add_input(pul1, 2)
    Tx2.add_output(pul2, 1)
    Tx2.add_output(pul3, 1)
    Tx2.sign(pr1)

    Tx3 = Tx()
    Tx3.add_input(pul3, 1.2)
    Tx3.add_output(pul1, 1.1)
    Tx3.add_reqd(pul4)
    Tx3.sign(pr3)
    Tx3.sign(pr4)

    for t in [Tx1, Tx2, Tx3]:
        if t.is_valid():
            print("Success! Tx is valid")
        else:
            print("ERROR! Tx is invalid")

    # Wrong Signatures
    Tx4 = Tx()
    Tx4.add_input(pul1, 1)
    Tx4.add_output(pul2, 1)
    Tx4.sign(pr2)

    # Escrow Tx not signed by the arbite
    Tx5 = Tx()
    Tx5.add_input(pul3, 1.2)
    Tx5.add_output(pul1, 1.1)
    Tx5.add_reqd(pul4)
    Tx5.sign(pr3)

    # Two input addrs, signed by one
    Tx5 = Tx()
    Tx5.add_input(pul3, 1)
    Tx5.add_output(pul4, 0.1)
    Tx5.add_output(pul1, 1.1)
    Tx5.sign(pr3)

    # Outputs exceed inputs
    Tx6 = Tx()
    Tx6.add_input(pul4, 1.2)
    Tx6.add_output(pul1, 1)
    Tx6.add_output(pul2, 2)
    Tx6.sign(pr4)

    # Negative 
    Tx7 = Tx()
    Tx7.add_input(pul2, -1)
    Tx7.add_output(pul1, -1)
    Tx7.sign(pr2)

    for t in [Tx4, Tx2, Tx3, Tx5, Tx6, Tx7]:
        if t.is_valid():
            print("ERROR! Bad Tx is valid")
        else:
            print("Success! Bad Tx is invalid")