#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import math
import random
import string

import FFX


def random_string(length, radix):
    retval = ''
    chars = string.digits + string.ascii_letters
    chars = chars[:radix]
    for i in range(length):
        index = random.randint(0,len(chars)-1)
        retval += chars[index]
    return retval


def main():
    radix = 2
    keysize = 128
    tweaksize = 8
    messagesize = 8
    
    banner = ['RADIX='+str(radix),
              'TWEAKSIZE='+str(tweaksize),
              'MESSAGESIZE='+str(messagesize),
             ]
    print ', '.join(banner)
    
    K = random_string(keysize, 2)
    K = string.rjust(K, keysize, '0')  # must be 128 bits, no matter what
    K = FFX.FFXInteger(K, radix=2, blocksize=keysize)
        
    for i in range(1,11):
        T = random_string(tweaksize, radix)
        M1 = random_string(messagesize, radix)

        T = string.rjust(T, tweaksize, '0')
        M1 = string.rjust(M1, messagesize, '0')

        T = FFX.FFXInteger(T, radix=radix, blocksize=tweaksize)
        M1 = FFX.FFXInteger(M1, radix=radix, blocksize=messagesize)

        ffx = FFX.new(radix)
        start = time.time()
        C = ffx.encrypt(K, T, M1)
        encrypt_cost = time.time() - start
        encrypt_cost *= 1000.0
        start = time.time()
        M2 = ffx.decrypt(K, T, C)
        decrypt_cost = time.time() - start
        decrypt_cost *= 1000.0

        assert M1 == M2
        
        to_print = ['tweak='+str(T),
                    'plaintext='+str(M1),
                    'ciphertext='+str(C),
                    'encrypt_cost='+str(round(encrypt_cost,1))+'ms',
                    'decrypt_cost='+str(round(decrypt_cost,1))+'ms',
                   ]
        print 'test #'+string.rjust(str(i),2,'0')+' SUCCESS: (' + ', '.join(to_print) + ')'


if __name__ == "__main__":
    main()
