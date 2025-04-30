from cryptography.fernet import Fernet, InvalidToken
from Logging import log

# ENCRYPTION
def encrypt_file(original_file_path, enc_file_path, enc_key_path):
    key = Fernet.generate_key()
    fernet = Fernet(key)
    message = ""
    try:
        message = open(original_file_path).read()
    except FileNotFoundError:
        log("ERROR : "+original_file_path+" not found\n")
        print("File not found")
        exit(1)

    # encrypt the message
    enc_message = fernet.encrypt(message.encode())
    print("encoded message: "+str(enc_message))
    try:
        with open(enc_file_path, "wb") as f:
            f.write(enc_message)
    except FileNotFoundError:
        log("ERROR : " + enc_file_path + " not found\n")
        print("File not found")
        exit(1)
    try:
        with open(enc_key_path, "wb") as f:
            f.write(key)
    except FileNotFoundError:
        log("ERROR : " + enc_key_path + " not found\n")
        print("File not found")
        exit(1)

# DECRYPTION
def decrypt_file(enc_file_path, enc_key_path):
    key = ""
    try:
        key = open(enc_key_path, "rb").read()
    except FileNotFoundError:
        log("ERROR : " + enc_key_path + " not found\n")
        print("File not found")
        exit(1)

    fernet = Fernet(key)

    # decrypt message
    dec_message = ""
    try:
        dec_message = fernet.decrypt(open(enc_file_path, "rb").read())
    except FileNotFoundError:
        log("ERROR : " + enc_file_path + " not found\n")
        print("File not found")
        exit(1)

    return dec_message.decode()

# encrypt original document and write the encryption key
# encrypt_file("normal_text_doc", "encrypted_text_doc", "encryption_key")

# decrypt the encrypted document using the encryption key
# print(decrypt_file("encrypted_text_doc", "encryption_key"))
