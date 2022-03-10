from cryptography.fernet import Fernet
import time
cipher_key = b'FpTcJt2CLjXZLbJCwNhFHrZt9A7XfhemCCWHlsD8jtA='
#cipher_key = Fernet.generate_key()
print(cipher_key)
#print(cipher_key)
cipher = Fernet(cipher_key)
#2016-04-07 10:25:09&01
print()
b = "2022-01-24 14:31:20&00002$$$002.txt&*"
b=bytes(b, encoding="utf8")
encrypted_text = cipher.encrypt(b)
print(encrypted_text)

decrypted_text = Fernet(b'NVY_cHeHMS5jXmfqQt7r-af5mbfPSdGtkN2nGsswf1s=').decrypt(b'gAAAAABiFL55h9RSIFg6CFhealzgdOEWg9SedXCZZDkBVBozE8G8QjISS-aeOrc5pn_1jSqbB3038kDb4UtxqWeTZou_SMq2rZ6tlG8vw8O3-5CLV1h5xSQ1laB5XouZIU27YtVp-l2NRMi6qGpU3y5q7lyLeIQsew==')

print(decrypted_text)
print(str(decrypted_text, encoding='utf-8'))
#print(bytes.decode(decrypted_text))