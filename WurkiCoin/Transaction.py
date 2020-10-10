# Transaction.py

import Signature
#Signature.sign
#Signature.verify

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

    ## Method to store Inbound Transactions
    def add_input(self, from_addr, amount, index=0):
        # Tuple: inputs will represent a list of tuples representing addr(string) & amounts(float)
        self.inputs.append((from_addr, amount, index))

    ## Method to store Outbound Transactions
    def add_output(self, to_addr, amount):
        self.outputs.append((to_addr, amount))

    ## Method to apply Required Signature to a Transaction
    def add_reqd(self, addr):
        self.reqd.append(addr)

    ## Method to apply Signature Transaction 
    def sign(self, private):
        message = self.__gather()
        newSig = Signature.sign(message, private)
        self.sigs.append(newSig)

    ## Method Confirms if Transaction is correctly assigned.
    def is_valid(self):
        total_in = 0
        total_out = 0
        message = self.__gather()
        # Self.inputs -> List[Tuples(addr, amount)]
        for addr, amount, index in self.inputs:
            found = False
            for s in self.sigs:
                if Signature.verify(message, s, addr):
                    found = True
            if not found:
                return False
            if amount < 0:
                return False
            total_in = total_out + amount

        for addr in self.reqd:
            found = False
            for s in self.sigs:
                if Signature.verify(message, s, addr):
                    found = True
            if not found:
                return False 

        for addr, amount in self.outputs:
            if amount < 0:
                return False
            total_out = total_out + amount

        ''' 
        # Remove as Miners best interest to have transactions where outputs > inputs.
        # Miners will be performing these checks.
        if total_out > total_in:
            return False
        '''
        return True

    # Private Member Function to Tx class. Collects data.
    def __gather(self):
        data = []
        data.append(self.inputs)
        data.append(self.outputs)
        data.append(self.reqd)
        return data

    # Called when converting to a string
    def __repr__(self):
        reprstr = "INPUTS:\n"
        for addr,amt,index in self.inputs:
            reprstr = reprstr + str(amt) + " from " + str(addr) + " index = " + str(index) + "\n"
        
        reprstr = reprstr + "OUTPUTS:\n"
        for addr,amt in self.outputs:
            reprstr = reprstr + str(amt) + " to " + str(addr) + "\n"

        reprstr = reprstr + "REQD:\n"
        for r in self.reqd:
            reprstr = reprstr + str(r) + "\n"

        reprstr = reprstr + "SIGS:\n"
        for s in self.sigs:
            reprstr = reprstr + str(s) + "\n"

        reprstr = reprstr + "END\n"

        return reprstr




# Testing
if __name__ == "__main__":
    pr1, pul1 = Signature.generate_keys()
    pr2, pul2 = Signature.generate_keys()
    pr3, pul3 = Signature.generate_keys()
    pr4, pul4 = Signature.generate_keys()

    # Correct Transactions 
    #Single Transaction between 2 Parties
    Tx1 = Tx()
    Tx1.add_input(pul1, 1)
    Tx1.add_output(pul2, 1)
    Tx1.sign(pr1)
    #Multiple Transaction between 3 Parties
    Tx2 = Tx()
    Tx2.add_input(pul1, 2)
    Tx2.add_output(pul2, 1)
    Tx2.add_output(pul3, 1)
    Tx2.sign(pr1)
    #Escrow Transaction
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
    # Escrow Tx not signed by the assigned arbiter
    Tx5 = Tx()
    Tx5.add_input(pul3, 1.2)
    Tx5.add_output(pul1, 1.1)
    Tx5.add_reqd(pul4)
    Tx5.sign(pr2)
    # Two input addrs, signed by one
    Tx6 = Tx()
    Tx6.add_input(pul3, 1)
    Tx6.add_input(pul4, 0.1)
    Tx6.add_output(pul1, 1.1)
    Tx6.sign(pr3)
    # 
    Tx7 = Tx()
    Tx7.add_input(pul3, 1)
    Tx7.add_output(pul4, 0.1)
    Tx7.add_output(pul1, 1.1)
    Tx7.sign(pr3)
    tmp = Tx7.inputs[0]
    Tx7.inputs[0] = (tmp[0], tmp[1], 78)
    # Negative 
    Tx8 = Tx()
    Tx8.add_input(pul2, -1)
    Tx8.add_output(pul1, -1)
    Tx8.sign(pr2)
    # Tamper - Modifying after Signature
    Tx9 = Tx()
    Tx9.add_input(pul1, 1)
    Tx9.add_output(pul2, 1)
    Tx9.sign(pr1)
    Tx9.outputs[0] = (pul3,1) # outputs = [(pul2, 1)] -- Modify -- [(pul3, 1)]

    for t in [Tx4, Tx5, Tx6, Tx8, Tx9]:
        if t.is_valid():
            print("ERROR! Bad Tx is valid")
        else:
            print("Success! Bad Tx is invalid")