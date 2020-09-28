# BlockChain.py
# BlockChain representation: [ hash | data] <-- [hash | data ] <-- [hash | data] <-- ... <-- [hash | data] 

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

class CBlock:
    previousHash = None
    def __init__(self, data=None, previousBlock=None):
        self.data = data
        self.previousBlock = previousBlock

        if previousBlock != None:
            self.previousHash = previousBlock.computeHash()

    def computeHash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data), 'utf-8'))
        digest.update(bytes(str(self.previousHash), 'utf-8'))
        
        return digest.finalize()

    def is_valid(self):
        #DANGEROUS TO DUE --> Only one valid with previous block of None is the Genesis Block
        if self.previousBlock.computeHash() == None:
            return True
        return self.previousBlock.computeHash() == self.previousHash

class someClass:
    num = 328965
    def __init__(self, mystring=None):
        self.string = mystring

    def __repr__(self):
        return self.string + "^^^" + str(self.num)


# Testing
if __name__ == '__main__':
    # Chain Of Blocks - pass in strings, class instance, integers.
    root = CBlock('I am root.', None)
    B1 = CBlock('I am a child.', root)
    B3 = CBlock(12354, B1)
    B2 = CBlock('I am B1s brother', root)
    B4 = CBlock(someClass('Hi there!'), B2)
    B5 = CBlock("Top block", B4)
    
    # Hash Success Detection
    for b in [B1, B2, B3, B4]:
        if b.previousBlock.computeHash() == b.previousHash:
            print('Success! Hash is good.')
        else:
            print('ERROR! Hash is no good.')

    # Tampering Detection
    # NOTE: For B4 Example below - Class variables are mutable by any instance of the class. While instance variables are mutable only by the instance of each class.
    # B4.data.num will change num class variable for all instances of the class.
    B2.data = 123456
    if B4.previousBlock.computeHash() == B4.previousHash:
        print('ERROR! Could not detect tampering.')
    else:
        print('Success! Tampering detected.')
    B4.data.num = 9999999
    if B5.previousBlock.computeHash() == B5.previousHash:
        print('ERROR! Could not detect tampering.')
    else:
        print('Success! Tampering detected.')