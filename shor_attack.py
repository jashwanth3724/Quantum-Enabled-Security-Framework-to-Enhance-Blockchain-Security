import random
import math


def find_period(a, N):

    r = 1

    while pow(a, r, N) != 1:
        r += 1

    return r


def shor_factor(N):

    while True:

        a = random.randint(2, N - 1)

        if math.gcd(a, N) != 1:
            return math.gcd(a, N), N // math.gcd(a, N)

        r = find_period(a, N)

        if r % 2 != 0:
            continue

        x = pow(a, r // 2, N)

        p = math.gcd(x - 1, N)
        q = math.gcd(x + 1, N)

        if p != 1 and q != 1:
            return p, q