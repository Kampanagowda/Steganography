import hashlib
import os.path
import numpy as np
from Crypto.Cipher import AES
from PIL import Image


class Decode:
    def __init__(self, image_path, password):
        self.image_path = image_path
        self.password = password.strip()

    def is_password_valid(self):
        if len(self.password) == 0:
            return False
        return True

    def is_image_path_valid(self):
        if os.path.exists(self.image_path):
            return True
        return False

    def get_decoded_text(self, bytes_string):
        secret_key = hashlib.sha1(str(self.password).encode()).hexdigest()[:32]
        decryption_key = AES.new(secret_key.encode('utf-8'), AES.MODE_EAX, secret_key.encode())
        bytes_value = eval(bytes_string)
        return decryption_key.decrypt(bytes_value).decode('utf-8')

    def decode_from_image(self):
        try:
            raw_image = Image.open(self.image_path, 'r')
            channels = 3
            if raw_image.mode == 'RGBA':
                channels = 4
            image_array = np.array(list(raw_image.getdata()))
            image_size = image_array.size // channels
            secret_hash = str(int(hashlib.md5(self.password.encode('utf-8')).hexdigest(), 16))[:5]
            if int(secret_hash) > image_size:
                secret_hash = secret_hash[:4]
                if int(secret_hash) > image_size:
                    secret_hash = secret_hash[:3]
                    if int(secret_hash) > image_size:
                        secret_hash = secret_hash[:2]
                        if int(secret_hash) > image_size:
                            secret_hash = secret_hash[:1]
                            if int(secret_hash) > image_size:
                                return ["Encoded text not found. The possible reasons might be:\n"
                                        "\n1. Incorrect Password"
                                        "\n2. Wrong Image", False]
            binary_value = ""
            for pixel in range(int(secret_hash), image_size):
                for channel in range(0, channels):
                    binary_value += bin(image_array[pixel][channel])[-1]

            for pixel in range(int(secret_hash)):
                for channel in range(0, channels):
                    binary_value += bin(image_array[pixel][channel])[-1]

            binary_list = [binary_value[value:value + 8] for value in range(0, len(binary_value), 8)]
            decoded_text = ""
            for i in range(len(binary_list)):
                if decoded_text[-4:] == "$@&#":
                    break
                else:
                    decoded_text += chr(int(binary_list[i], 2))

            if "$@&#" in decoded_text:
                decoded_text = decoded_text[:-4]
                try:
                    decoded_text = self.get_decoded_text(decoded_text)
                    return [decoded_text, True]
                except UnicodeDecodeError:
                    return ["Encoded text not found. The possible reasons might be:\n"
                            "\n1. Incorrect Password"
                            "\n2. Wrong Image", False]
            else:
                return ["Encoded text not found. The possible reasons might be:\n"
                        "\n1. Incorrect Password"
                        "\n2. Wrong Image", False]
        except Exception:
            return ["Encoded text not found. The possible reasons might be:\n"
                    "\n1. Incorrect Password"
                    "\n2. Wrong Image", False]

    def are_values_valid(self):
        if not self.is_password_valid():
            return ["Password can't be empty.", False]
        elif not self.is_image_path_valid():
            return ["Selected image doesn't exist anymore.", False]
        else:
            return ["Valid", True]
