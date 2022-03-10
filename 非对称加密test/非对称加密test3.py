from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

#生成密钥
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()
# store private key
private_key1 = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
public_key1 = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)



print(public_key1)
a=bytes('0024',encoding='utf-8')+public_key1
if a[0:4]==bytes('0024',encoding='utf-8'):
    a=a[4:]
public_key1=a
print(public_key1)



public_key2 = serialization.load_pem_public_key(
        public_key1,
        backend=default_backend()
    )

message = b'123456789012345678901234567890123456789012345678901234567890123456789012345667890123456789012345678901234567890123456789012345678901234566789012345678901234567890123456789012345678901234567890123456678901234567890123456789012345678901234567890123456789012345667890123456789012345678901234567890123456789012345678901234566789012345678901234567890123456789012345678901234567890123456678901234567890123456789012345678901234567890123456789012345667890123456789012345678901234567890123456789012345678901234566789012345678901234567890123456789012345678901234567890123456678901234567890123456789012345678901234567890123456789012345667890123456789012345678901234567890123456789012345678901234566789012345678901234567890123456789012345678901234567890123456678901234567890123456789012345678901234567890123456789012345667890123456789012345678901234567890123456789012345678901234566789012345678901234567890123456789012345678901234567890123456678901234567890123456789012345678901234567890123456789012345667890123456789012345678901234567890123456789012345678901234566789012345678901234567890123456789012345678901234567890123456678901234567890123456789012345678901234567890123456789012345667890123456789012345678901234567890123456789012345678901234566789012345678901234567890123456789012345678901234567890123456678901234567890123456789012345678901234567890123456789012345667890123456789012345678901234567890123456789012345678901234566789012345678901234567890123456789012345678901234567890123456678901234567890123456789012345678901234567890123456789012345667890123456789012345678901234567890123456789012345678901234566789012345678901234567890123456789012345678901234567890123456678901234567890123456789012345678901234567890123456789012345667890123456789012345678901234567890123456789012345678901234566789012345678901234567890123456789012345678901234567890123456678901234567890123456789012345678901212345667890123456789012345678901234567890121234566789012345678901234567890123456789012123456678901234567890123456789012345678901212345667890123456789012345678901234567890121234566789012345678901234567890123456789012123456678901234567890123456789012345678901212345667890123456789012345678901234567890121234566789012345678901234567890123456789012345678901234567890123456678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
print(len(message))
encrypted=b''
if len(message) <= 150:
    encrypted = public_key2.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
while len(message)>150:
    message1=message[:150]
    encrypting = public_key2.encrypt(
        message1,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    encrypted=encrypted+ b'&&&'+encrypting
    message=message[150:]
    if len(message)<=150:
        encrypting = public_key2.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        encrypted = encrypted + b'&&&'+encrypting
        break



print(encrypted)
private_key2 = serialization.load_pem_private_key(
        private_key1,
        password=None,
        backend=default_backend()
    )
original_message=b''
if encrypted[:3]==b'&&&':
    i=3
    beginnum=3
    while i<len(encrypted):
            print(encrypted[i:i+3])

            if encrypted[i:i+3]==b'&&&':
                decrypting=encrypted[beginnum:i]
                original_message1 = private_key2.decrypt(
                    decrypting,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                original_message=original_message+original_message1
                beginnum=i+3
            i=i+1
    decrypting = encrypted[beginnum:]
    original_message1 = private_key2.decrypt(
        decrypting,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    original_message = original_message + original_message1
else:
    original_message = private_key2.decrypt(
                    encrypted,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )



print(original_message)