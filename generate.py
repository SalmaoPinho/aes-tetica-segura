import os
# RSA
from cryptography.hazmat.primitives.asymmetric import rsa
# PEM
from cryptography.hazmat.primitives import serialization


#ini importer
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

def gen_rsa():
    private_key = rsa.generate_private_key(
        public_exponent=int(config["RSA"]["public_exponent"]),
        key_size=int(config["RSA"]["key_size"]),
    )
    public_key = private_key.public_key()
    return private_key, public_key

def pemfile():
    os.makedirs("keys", exist_ok=True)
    #chaves privadas pra empresa a e b
    A=gen_rsa()
    B=gen_rsa()
    pemA=A[0].private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    pemB=B[0].private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open("keys/empresaAprivate.pem", "wb") as f:
        f.write(pemA)
    with open("keys/empresaBprivate.pem", "wb") as f:
        f.write(pemB)
    
    #chaves publicas pra empresa a e b
    pemA=A[1].public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    pemB=B[1].public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open("keys/empresaApublic.pem", "wb") as f:
        f.write(pemA)
    with open("keys/empresaBpublic.pem", "wb") as f:
        f.write(pemB)
    print("Chaves geradas e salvas na pasta keys/")


pemfile()