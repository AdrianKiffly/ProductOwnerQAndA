import os
from Encryption import decrypt_file
from Logging import log

from cryptography.fernet import Fernet, InvalidToken
import google.genai as genai
from httpx import ConnectError, RemoteProtocolError
from dotenv import load_dotenv

def main():
    # Check if Token (enc file) and if key (enc key) is correct
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
    # Start of infinite loop
    while True:
        print("What would you like to know about the document?")
        # Ensure that if the program stop halfway, it would gracefully exit
        try:
            question = input("> ")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            exit(0)
        # allow user to exit without stopping the program
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
            # Catch connection error
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