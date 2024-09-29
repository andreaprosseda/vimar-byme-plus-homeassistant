import subprocess
import base64
from .file import get_file_path
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.asymmetric.utils import Prehashed
# from cryptography.hazmat.primitives.asymmetric import padding
# from cryptography.hazmat.primitives.asymmetric import rsa
# from cryptography.hazmat.primitives import serialization
# from cryptography.hazmat.primitives.asymmetric.types import PrivateKeyTypes

def sign_vimar_code(code: str) -> str:
    private_key_pem = get_file_path("aprosseda.key.pem")
    return sign_code_openssl(code, private_key_pem)    

def sign_code_openssl(code: str, private_key_path: str) -> str:
    command = ["openssl", "pkeyutl", "-sign", "-inkey", private_key_path]
    result = subprocess.run(
        command,
        input=code.encode('utf-8'),
        capture_output=True,
        check=True
    )

    signature = result.stdout
    signature_b64 = base64.b64encode(signature).decode('utf-8')
    # print(f"Base64 Encoded Signature:\n{signature_b64}")
    return signature_b64

# def sign_code(code: str, private_key_path: str) -> str:
#     private_key = get_private_key(private_key_path)
#     print(private_key)
#     signature = sign(code, private_key)
#     print(signature)
#     signature_b64 = base64.b64encode(signature).decode('utf-8')
#     return signature_b64
# 
# def get_private_key(path: str) -> PrivateKeyTypes:
#     private_key = None
#     with open(path, 'rb') as key_file:
#         private_key: PrivateKeyTypes = serialization.load_pem_private_key(
#             key_file.read(),
#             password=None,
#             backend=default_backend()
#         )
#     return private_key
# 
# def sign(code: str, private_key: PrivateKeyTypes) -> bytes:
#     return private_key.sign(
#         code.encode('utf-8'),
#         padding.PKCS1v15(),
#         Prehashed(hashes.SHA256())
#     )