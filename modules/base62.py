# -*- coding: utf-8 -*-
########################################
#  credits: http://web.archive.org/web/20130525090551/http://blog.kevburnsjr.com/php-unique-hash
########################################
import collections
golden_primes1 = [('1', '1'),
                  ('41', '59'),
                  ('2377', '1677'),
                  ('147299', '187507'),
                  ('9132313', '5952585'),
                  ('566201239', '643566407'),
                  ('35104476161', '22071637057'),
                  ('2176477521929', '294289236153'),
                  ('134941606358731', '88879354792675'),
                  ('8366379594239857', '7275288500431249'),
                  ('518715534842869223', '280042546585394647')
                  ]

golden_primes = collections.OrderedDict(golden_primes1)

chars62 = range(48, 58) + range(65, 91) + range(97, 123)


def base62(intg):
    key = ""
    while intg > 0:
        mod = intg % 62
        key += str(unichr(chars62[mod]))
        intg = intg / 62
    return key[::-1]


def encode(num, len1=7):
    ceil = pow(62, len1)
    primes = golden_primes.keys()
    prime = int(primes[len1])
    dec = (num * prime) % ceil
    hash2 = base62(dec)
    return hash2.zfill(len1)


def unbase62(key):
    intg = 0
    reversed_key = key[::-1]
    for i, chart in enumerate(reversed_key):
        dec = chars62.index(ord(chart))
        intg = (dec * pow(62, i)) + intg

    return intg


def decode(hash2):
    len1 = len(hash2)
    ceil = pow(62, len1)
    mmiprimes = golden_primes.values()
    mmi = int(mmiprimes[len1])
    num = unbase62(hash2)
    dec = (num * mmi) % ceil
    return dec
