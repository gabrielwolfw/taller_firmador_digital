
import math


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


def generar_llaves(p, q, e):
    n = p * q
    phi = (p - 1) * (q - 1)

    assert 1 < e < phi, "e debe estar entre 1 y phi"
    assert math.gcd(e, phi) == 1, "e y phi deben ser coprimos"

    d = modinv(e, phi)
    return n, phi, d


def firmar(H, e, n):
    return pow(H, e, n)


def decifrar(C, d, n):
    return pow(C, d, n)


def verificar(H, S, d, n):
    H_decrypted = decifrar(S, d, n)
    return H == H_decrypted


def main():
    p = 61
    q = 53
    e = 17

    n, phi, d = generar_llaves(p, q, e)

    print(f"n   = {n}")
    print(f"e   = {e}")
    print(f"d   = {d}")
    print(f"phi = {phi}")
    print(f"Verificación: (e × d) % phi = {(e * d) % phi}")

    H = 123  # H es el hash del mensaje que queremos encriptar
    S = firmar(H, e, n)

    print(f"Hash H = {H}")
    print(f"Texto encriptado S = {S}")
    print(f"Verificación: {verificar(H, S, d, n)}")


if __name__ == "__main__":
    main()