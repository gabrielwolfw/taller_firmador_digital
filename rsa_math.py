import math

from solucion_rsa_core import generate_p_q, miller_rabin_probable_prime, modinv as _modinv


def egcd(a, b):
    # Caso base: si b llega a 0, terminamos
    if b == 0:
        return (a, 1, 0)  # (mcd, x, y)

    # Llamada recursiva
    g, x1, y1 = egcd(b, a % b)

    # Reconstruimos x e y hacia atrás
    x = y1
    y = x1 - (a // b) * y1

    return (g, x, y)


def modinv(e, phi):
    g, x, _ = egcd(e, phi)

    if g != 1:
        raise ValueError("e no es invertible módulo phi")

    return x % phi  # Garantiza que el resultado sea positivo


def generar_llaves(bits_primo=128, rounds=20, e=65537):
    p, q = generate_p_q(bits_primo, rounds=rounds)
    n = p * q
    phi = (p - 1) * (q - 1)

    assert 1 < e < phi, "e debe estar entre 1 y phi"
    assert math.gcd(e, phi) == 1, "e y phi deben ser coprimos"

    d = _modinv(e, phi)
    return n, phi, e, d


def firmar(H, d, n):
    return pow(H, d, n)


def decifrar(C, e, n):
    return pow(C, e, n)


def verificar(H, S, e, n):
    H_decrypted = decifrar(S, e, n)
    return H == H_decrypted


def main():
    # Parte 4: Generar claves con Miller-Rabin
    bits_primo = 128
    rounds = 20
    e_pub = 65537

    n, phi, e, d = generar_llaves(bits_primo=bits_primo, rounds=rounds, e=e_pub)

    print(f"n bits = {n.bit_length()}")
    print(f"n (hex prefijo) = {hex(n)[:26]}...")
    print(f"Checkpoint: (e * d) % phi = {(e * d) % phi}")

    compuesto = 3 * 999999999999999999
    print(f"miller_rabin_probable_prime({compuesto}) = {miller_rabin_probable_prime(compuesto, rounds=rounds)}")

    # Parte 3: Firma y verificacion sobre enteros H
    H = 123
    S = firmar(H, d, n)

    print(f"\nHash H = {H}")
    print(f"Firma S = {S}")
    print(f"Verificacion: {verificar(H, S, e, n)}")




if __name__ == "__main__":
    main()