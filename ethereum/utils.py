from eth_utils import big_endian_to_int, encode_hex
from web3._utils.normalizers import normalize_address

try:
    from Crypto.Hash import keccak


    def sha3_256(x):
        return keccak.new(digest_bits=256, data=x).digest()
except ImportError:
    import sha3 as _sha3


    def sha3_256(x):
        return _sha3.keccak_256(x).digest()


def to_string(value):
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return bytes(value, 'utf-8')
    if isinstance(value, int):
        return bytes(str(value), 'utf-8')


def sha3(seed):
    return sha3_256(to_string(seed))


def checksum_encode(addr):  # Takes a 20-byte binary address as input
    addr = normalize_address(addr)
    o = ''
    v = big_endian_to_int(sha3(encode_hex(addr)))
    for i, c in enumerate(encode_hex(addr)):
        if c in '0123456789':
            o += c
        else:
            o += c.upper() if (v & (2 ** (255 - 4 * i))) else c.lower()
    return '0x' + o


def remove_0x_head(s):
    return s[2:] if s[:2] in (b'0x', '0x') else s
