import hashlib
import os.path
import numpy as np
from Crypto.Cipher import AES
from PIL import Image


class Encode:
    def __init__(self, image_path, password, text_to_encode):
        self.image_path = image_path
        self.password = password.strip()
        self.text_to_encode = text_to_encode.strip()

    def is_password_valid(self):
        if len(self.password) == 0:
            return False
        return True

    def is_text_valid(self):
        if len(self.text_to_encode) == 0:
            return False
        return True

    def is_image_path_valid(self):
        if os.path.exists(self.image_path):
            return True
        return False

    def get_text_binary(self):
        secret_key = hashlib.sha1(str(self.password).encode()).hexdigest()[:32]
        encryption_key = AES.new(secret_key.encode('utf-8'), AES.MODE_EAX, secret_key.encode())
        encrypted_text = encryption_key.encrypt(self.text_to_encode.encode('utf-8'))
        encrypted_text = str(encrypted_text)
        encrypted_text += "$@&#"
        binary_value = ''.join([format(ord(character), "08b") for character in encrypted_text])
        return binary_value

    def encode_into_image(self):
        try:
            raw_image = Image.open(self.image_path, 'r')
            width, height = raw_image.size
            channels = 3
            if raw_image.mode == 'RGBA':
                channels = 4
            image_array = np.array(list(raw_image.getdata()))
            image_size = image_array.size // channels
            binary_value = self.get_text_binary()
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
                                return ['Image size is not sufficient to encode the given text.', False]
            text_size = len(binary_value)
            encode_space = image_size - int(secret_hash)
            retro_encode = False
            if text_size > encode_space:
                retro_encode = True
            if text_size > image_array.size:
                return ['Image size is not sufficient to encode the given text.', False]
            else:
                bin_index = 0
                for pixel in range(int(secret_hash), image_size):
                    for channel in range(0, channels):
                        if bin_index < text_size:
                            image_array[pixel, channel] = int(bin(image_array[pixel][channel])[2:9] +
                                                              binary_value[bin_index], 2)
                            bin_index += 1

                if retro_encode:
                    for pixel in range(int(secret_hash)):
                        for channel in range(0, channels):
                            if bin_index < text_size:
                                image_array[pixel, channel] = int(bin(image_array[pixel][channel])[2:9] +
                                                                  binary_value[bin_index], 2)
                                bin_index += 1

                image_array = image_array.reshape(height, width, channels)
                stego_image = Image.fromarray(image_array.astype('uint8'), raw_image.mode)
                return [stego_image, True]
        except Exception:
            return ['Unidentified Error. The possible reasons might be\n'
                    '\n1. Unsupported Image File'
                    '\n2. Invalid text characters', False]

    def are_values_valid(self):
        if not self.is_password_valid():
            return ["Password can't be empty.", False]
        elif not self.is_text_valid():
            return ["Text to encode can't be empty.", False]
        elif not self.is_image_path_valid():
            return ["Selected image doesn't exist anymore.", False]
        else:
            return ["Validated", True]
