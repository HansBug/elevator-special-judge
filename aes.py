import base64
import binascii

from Crypto.Cipher import AES

__key = b"#I88--_NrPAqCm9N"


def __base64_decode(s):
    try:
        return base64.urlsafe_b64decode(s)
    except binascii.Error:
        padding = len(s) % 4
        if padding == 1:
            raise ValueError('Invalid base64 string')
        elif padding == 2:
            s += '=='
        elif padding == 3:
            s += '='
        return base64.urlsafe_b64decode(s)


def __unpad(s):
    return s[:-ord(s[len(s) - 1:])]


def decrypt(encrypted_with_iv):
    encrypted_with_iv = __base64_decode(encrypted_with_iv)
    iv = encrypted_with_iv[:16]
    encrypted = encrypted_with_iv[16:]
    decrypt_helper = AES.new(__key, AES.MODE_CFB, iv, segment_size=128)
    decrypted = __unpad(decrypt_helper.decrypt(encrypted))
    return bytes.decode(decrypted).strip()
