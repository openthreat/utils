#!/usr/bin/env python
import hashlib
import os
import string
import sys

base = string.printable.strip()  # strip line feed
base = string.digits + string.letters + '=!()[]?;:_<>'  # TV mode
secret_location = '.password.secret'

def convert_to_base(binary, base):
    base_len = len(base)
    digit = int(binary.encode('hex'), 16)

    new_base = ''
    while digit > 0:
        remainder = digit % base_len
        new_base += base[remainder]
        digit = digit // base_len

    return new_base[::-1]


def generate(env, salt):
    global base
    dk = hashlib.pbkdf2_hmac('sha256', env, salt, 100000)
    # binascii.hexlify(dk)
    return convert_to_base(dk, base)


if __name__ == '__main__':
    os_args = sys.argv
    if len(os_args) != 2:
        raise Exception('Need env param')


    if not os.path.exists(secret_location):
        binary_salt = ''.join([c for c in os.urandom(32)])
        with open(secret_location, 'w') as f:
            f.write(''.join(binary_salt))

    salt = open(secret_location).read()

    chash = generate(os_args[1], salt)
    print chash[:12]
    print chash
