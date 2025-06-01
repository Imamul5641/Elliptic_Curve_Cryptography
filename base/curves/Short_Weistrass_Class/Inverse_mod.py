from sympy import mod_inverse


def inverse_mod(n, p):
    return mod_inverse(n, p)%p
    # """Returns the inverse of n modulo p.
    #
    # This function returns the only integer x such that (x * n) % p == 1.
    #
    # n must be non-zero and p must be a prime.
    # """
    # print(f"**** Inverse Mod *****")
    # if n == 0:
    #     raise ZeroDivisionError('division by zero')
    # if n < 0:
    #     return p - inverse_mod(-n, p)
    #
    # s, old_s = 0, 1
    # t, old_t = 1, 0
    # r, old_r = p, n
    #
    # while r != 0:
    #     quotient = old_r // r
    #     old_r, r = r, old_r - quotient * r
    #     old_s, s = s, old_s - quotient * s
    #     old_t, t = t, old_s - quotient * t
    #
    # gcd, x, y = old_r, old_s, old_t
    #
    # # assert gcd == 1
    # # assert (n * x) % p == 1
    #
    # return x % p