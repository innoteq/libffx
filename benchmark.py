#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
import time
import random
import string
import argparse

import ffx
from ffx import FFXInteger
from six.moves import range


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--radix", type=int, default=2)
    parser.add_argument("--tweaksize", type=int, default=8)
    parser.add_argument("--messagesize", type=int, default=32)
    parser.add_argument("--trials", type=int, default=10, required=False)
    args = parser.parse_args()

    radix = args.radix
    tweaksize = args.tweaksize
    messagesize = args.messagesize
    trials = args.trials

    keysize = 128
    K = random.randint(0, 2 ** keysize - 1)
    K = FFXInteger(K, radix=2, blocksize=keysize)

    banner = ['RADIX=' + str(radix),
              'TWEAKSIZE=' + str(tweaksize),
              'MESSAGESIZE=' + str(messagesize),
              'KEY=' + hex(K.to_int())
              ]
    print(', '.join(banner))

    ffx_obj = ffx.new(K.to_bytes(), radix)
    for i in range(1, trials):
        T = random.randint(0, radix ** tweaksize - 1)
        T = FFXInteger(T, radix=radix, blocksize=tweaksize)

        M1 = random.randint(0, radix ** messagesize - 1)
        M1 = FFXInteger(M1, radix=radix, blocksize=messagesize)

        start = time.time()
        C = ffx_obj.encrypt(T, M1)
        encrypt_cost = time.time() - start
        encrypt_cost *= 1000.0

        start = time.time()
        M2 = ffx_obj.decrypt(T, C)
        decrypt_cost = time.time() - start
        decrypt_cost *= 1000.0

        assert M1 == M2

        to_print = ['encrypt_cost=' + str(round(encrypt_cost, 1)) + 'ms',
                    'decrypt_cost=' + str(round(decrypt_cost, 1)) + 'ms',
                    'tweak=' + str(T),
                    'plaintext=' + str(M1),
                    'ciphertext=' + str(C),
                    ]
        print('test #' + string.rjust(str(i), len(str(trials - 1)), '0') + ' SUCCESS: (' + ', '.join(to_print) + ')')


if __name__ == "__main__":
    main()
