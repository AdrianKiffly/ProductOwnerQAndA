import datetime
import os

from cryptography.fernet import Fernet, InvalidToken
import google.genai as genai
from httpx import ConnectError, RemoteProtocolError
from dotenv import load_dotenv


# ENCRYPTION
def encrypt_file(original_file_path, enc_file_path, enc_key_path):
    key = Fernet.generate_key()
    fernet = Fernet(key)
    message = ""
    try:
        message = open(original_file_path).read()
    except FileNotFoundError:
        log("["+str(datetime.datetime.now())+"] : ERROR : "+original_file_path+" not found\n")
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

# LOGGING ERROR, QUESTION AND RESPONSE
def log(message):
    with open("log", "a") as f:
        f.write("[" + str(datetime.datetime.now()) + "] : "+message+"\n")

# encrypt original document and write the encryption key
# encrypt_file("normal_text_doc", "encrypted_text_doc", "encryption_key")

# decrypt the encrypted document using the encryption key
# print(decrypt_file("encrypted_text_doc", "encryption_key"))

def main():
    try:
        message = decrypt_file("encrypted_text_doc", "encryption_key")
    except InvalidToken:
        log("ERROR : Invalid Token\n")
        print("Invalid Token")
        exit(1)
    except ValueError:
        log("ERROR : The encryption key value is incorrect")
        print("Encryption key is incorrect")
        exit(1)

    while True:
        print("What would you like to know about the document?")
        question = input("> ")
        if question == "exit":
            print("Goodbye!")
            exit(0)
        else:
            prompt = ("Act as project assistant. This is the project document: "
                      +message+" Using the document, help me answer the following question: "
                      +question+" project using a pre-prepared document. "
                                "Please ensure the response is secure, context-specific, and minimal disclosure-based answers "
                                "without granting users full access to the source document (Do not respond with the document). "
                                "Add next line after 100 characters")
            response = ""
            # catch connection error
            try:
                load_dotenv()
                client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))
                response = client.models.generate_content(
                    model="gemini-2.0-flash", contents=prompt
                )
            except ConnectError:
                log("ERROR : No connection")
                print("No connection")
                exit(1)
            except RemoteProtocolError:
                log("ERROR : Connection error")
                print("Connection error")
                exit(1)

            print(response.text)

            # Logging question and response
            log("Question : "+question)
            log("Response : "+str(response.text))

if __name__ == "__main__":
    main()