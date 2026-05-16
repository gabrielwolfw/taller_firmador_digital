#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import math
import secrets

from sympy.ntheory.primetest import mr


def egcd(a: int, b: int) -> tuple[int, int, int]:
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)


def modinv(e: int, phi: int) -> int:
    g, x, _ = egcd(e % phi, phi)
    if g != 1:
        raise ValueError("e no es invertible modulo phi")
    return x % phi


def random_odd(bits: int) -> int:
    if bits < 2:
        raise ValueError("bits >= 2")
    while True:
        x = secrets.randbits(bits)
        x |= (1 << (bits - 1)) | 1
        if x.bit_length() == bits:
            return x


def miller_rabin_probable_prime(n: int, rounds: int = 24) -> bool:
    if n < 2 or n % 2 == 0:
        return n == 2
    if n == 3:
        return True
    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2
        if not mr(n, [a]):
            return False
    return True


def generate_prime(bits: int, rounds: int = 24) -> int:
    while True:
        c = random_odd(bits)
        if miller_rabin_probable_prime(c, rounds=rounds):
            return c


def generate_p_q(bits_primo: int, rounds: int = 24) -> tuple[int, int]:
    p = generate_prime(bits_primo, rounds=rounds)
    while True:
        q = generate_prime(bits_primo, rounds=rounds)
        if q != p:
            return p, q


def main() -> None:
    bits_primo = 128
    rounds = 20
    e = 65537

    p, q = generate_p_q(bits_primo, rounds=rounds)
    n = p * q
    phi = (p - 1) * (q - 1)
    if not (1 < e < phi) or math.gcd(e, phi) != 1:
        raise SystemExit("Elija otro e coprimo con phi (p.ej. 17 en juguete)")
    d = modinv(e, phi)

    assert (e * d) % phi == 1
    print(f"p bits={p.bit_length()}, q bits={q.bit_length()}")
    print(f"n bits={n.bit_length()}, n (hex prefijo)={hex(n)[:26]}...")
    print("Checkpoint OK: (e * d) % phi == 1")


if __name__ == "__main__":
    main()
