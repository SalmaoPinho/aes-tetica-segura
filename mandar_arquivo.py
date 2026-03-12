import socket
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

HOST = "127.0.0.1"
PORT = 5000

with open("keys/empresaBpublic.pem", "rb") as f:
    public_key = RSA.import_key(f.read())

aes_key = get_random_bytes(32)

cipher_rsa = PKCS1_OAEP.new(public_key)
aes_encriptado = cipher_rsa.encrypt(aes_key)

with open("docs/bomdia.pdf", "rb") as file:
    data = file.read()

cipher = AES.new(aes_key, AES.MODE_GCM)
ciphertext, tag = cipher.encrypt_and_digest(data)

payload = (
    len(aes_encriptado).to_bytes(4, "big") +
    aes_encriptado +
    cipher.nonce +
    tag +
    ciphertext
)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(payload)

print("Arquivo enviado")