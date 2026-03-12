import socket
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

HOST = "127.0.0.1"
PORT = 5000

with open("keys/empresaBprivate.pem", "rb") as f:
    private_key = RSA.import_key(f.read())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)

    print("Aguardando conexao...")

    conn, addr = s.accept()

    with conn:
        print("Conectado por", addr)

        data = b""
        while True:
            packet = conn.recv(4096)
            if not packet:
                break
            data += packet

tam = int.from_bytes(data[:4], "big")
pos = 4

aes_encriptado = data[pos:pos+tam]
pos += tam

nonce = data[pos:pos+16]
pos += 16

tag = data[pos:pos+16]
pos += 16

ciphertext = data[pos:]

cipher_rsa = PKCS1_OAEP.new(private_key)
aes_key = cipher_rsa.decrypt(aes_encriptado)

cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)

try:
    arquivo = cipher.decrypt_and_verify(ciphertext, tag)

    with open("docs/arquivo_recebido.pdf", "wb") as f:
        f.write(arquivo)

    print("Arquivo recebido e salvo com sucesso")

except ValueError:
    print("Falha na autenticação")