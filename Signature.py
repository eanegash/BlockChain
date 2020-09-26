# Signature.py

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature


## Generate a new RSA private key using the provided backend.
def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent = 65537,
        key_size = 2048,
        backend = default_backend()
    )

    public_key = private_key.public_key()
    
    return private_key, public_key

## Private key is used to sign a message. This allows anyone with the public key to verify that the message 
## was created by someone who possesses the corresponding private key. 
def sign(message, private_key):
    # Converting to str to a byte to deal with passed in messages already encoded in bytes.  
    message = bytes(str(message), 'utf-8')
    sig = private_key.sign(
        message,
        # SALT and HASH
        padding.PSS(
            mgf = padding.MGF1(hashes.SHA256()),
            salt_length = padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return sig

## Verifies that the private key associated with a given public key was used to sign the message.
def verify(message, sig, public):
    message = bytes(str(message), 'utf-8')
    try:
        public.verify(
            sig,
            message,
            padding.PSS(
                mgf = padding.MGF1(hashes.SHA256()),
                salt_length = padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature: 
        return False
    except:
        print("Error executing public_key.verify")
        return False

# Tests
if __name__ == "__main__":
    pr, pu = generate_keys()

    message = b"Automated processess, machine learning, security, and blockchain. Lets build some great things."
    sig = sign(message, pr)
    correct = verify(message, sig, pu)

    if correct:
        print("Good sig.")
    else:
        print("Sig is bad.")   
