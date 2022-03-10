from cryptography.fernet import Fernet
while True:
 cipher_key = Fernet.generate_key()
 print(str(cipher_key,encoding='utf-8'))