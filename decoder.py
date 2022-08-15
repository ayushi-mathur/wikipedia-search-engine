import string

ALPHABET = "".join([string.digits, string.ascii_lowercase, string.ascii_uppercase, '+_'])
ALPHABET_REVERSE = dict((c, i) for (i, c) in enumerate(ALPHABET))
BASE = len(ALPHABET)

def num_decode(s):
    n = 0
    for c in s:
        n = n * BASE + ALPHABET_REVERSE[c]
    return n

n = input()
print(num_decode(n))