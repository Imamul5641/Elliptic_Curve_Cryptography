def compute_order(curve, P, N):
    """Computes the order n of point P, given N = #E(F_p)."""
    print(f"**** Compute Order *****")
    if P is None:
        return 1  # Order of the point at infinity is 1

    # Step 1: Factorize N into its prime factors
    def factorize(n):
        factors = []
        # Handle 2 separately
        while n % 2 == 0:
            factors.append(2)
            n = n // 2
        # Check odd divisors up to sqrt(n)
        i = 3
        while i * i <= n:
            while n % i == 0:
                factors.append(i)
                n = n // i
            i += 2
        if n > 1:
            factors.append(n)
        return factors

    prime_factors = factorize(N)

    # Step 2: Generate all divisors of N in sorted order
    def get_divisors(factors):
        divisors = [1]
        for p in factors:
            new_divisors = []
            for d in divisors:
                new_divisors.append(d * p)
            divisors += new_divisors
        return sorted(set(divisors))  # Remove duplicates and sort

    divisors = get_divisors(prime_factors)

    # Step 3: Find the smallest d where dP = O
    for d in divisors:
        if curve.mult(d, P) is None:
            return d


    return N  # Fallback (if P is a generator, n = N)

# Define the order-finding function
def point_order(curve, xp, yp):
    xq, yq = xp, yp
    point = curve.add( (xq, yq) , (xq, yq) )  # First doubling
    if point==None:
        return 1
    xr, yr = point
    order = 2

    while (xr != xp or yr != yp):
        xq, yq = xr, yr
        point = curve.add( ( xp, yp) , ( xq, yq) )
        order += 1

        if point == None:
            return order

        xr, yr = point

    return order