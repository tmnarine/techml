#
# spigotpi.py -- generate pi using the spigot algorithm
#
# http://stanleyrabinowitz.com/bibliography/spigot.pdf
# - contains Pascal version of the algorithm
#

import math

# Available on the web
def pi_as_str():
    return "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"


def spigotpi(N, printResult, debugInfo = False):
    
    assert(N > 0)

    # lowlevel reduces the operation into smaller tasks that
    # can be replicated in assembler
    use_lowlevel = True

    def calcLen():
        if use_lowlevel:
            result = 0
            u = N
            v = 0
            while u >= 3:
                u -= 3
                v += 1
            result += (v << 3) + (v << 2) + 1
            
        return math.floor(10 * N / 3) + 1
    
    LEN = calcLen()
    A = [2 for i in range(0,LEN)]
    
    # print("LEN: ",LEN)
    
    nines = 0
    predigit = 0

    spigotpi_str = ""

    for j in range(1, N+1):
        q = 0
        for i in range(LEN, 0, -1):

            def calcX():
                if use_lowlevel:
                    result = 0
                    v = A[i-1]
                    result += (v << 3) + (v << 1)
                    for z in range(0,i):
                        result += q
                    return result
                
                return 10 * A[i-1] + q * i

            def calcPreviousA():
                if use_lowlevel:
                    result = 0
                    v = i<<1
                    v -= 1
                    u = x
                    while u >= v:
                        u -= v
                    result = u
                    return result
                
                return x % (2 * i - 1)

            def calcQ():
                if use_lowlevel:
                    result = 0
                    v = i<<1
                    v -= 1
                    u = x
                    while u >= v:
                        u -= v
                        result += 1
                    return result
                        
                return int(x / (2 * i -1))
            
            x = calcX()
            A[i-1] = calcPreviousA()
            q = calcQ()

        def calcA0():
            if use_lowlevel:
                u = q
                while u >= 10:
                    u -= 10
                return u
            
            return q % 10

        def calcQ2():
            if use_lowlevel:
                result = 0
                u = q >> 1
                while u >= 5:
                    u -= 5
                    result += 1
                return result
            
            return int(q / 10);
        
        A[0] = calcA0()
        q = calcQ2()

        if 9 == q:
            nines += 1
        else:
            newdigit = predigit+1 if 10 == q else predigit
            spigotpi_str += ("%d" % (newdigit))
            newdigit = 0 if 10 == q else 9
            for k in range(0, nines):
                spigotpi_str += ("%d" % (newdigit))
            predigit = 0 if 10 == q else q
            if 10 != q:
                nines = 0

        if debugInfo:
            print(A, spigotpi_str)

    spigotpi_str += ("%d" % (predigit))

    # Check the result

    pi_str = pi_as_str().replace(".", "")

    assert(N < len(pi_str))

    len_spigotpi_str = len(spigotpi_str)
    len_pi_str = len(pi_str)
    
    # Output
    ds = ("%d" % N)
    spacing = (" "*(8-len(ds))) if len(ds) < 8 else ""
    print("Spigotpi N = %s%s: " % (ds, spacing), end="")
    
    check_len = len_spigotpi_str if len_spigotpi_str < len_pi_str else len_pi_str
    for i in range(0, check_len-1):
        assert(pi_str[i] == spigotpi_str[i+1])
        if printResult:
            print("%s" % (spigotpi_str[i+1]), end="")

    print("")    
    
def main():
    spigotpi(1, True)
    spigotpi(2, True)
    spigotpi(3, True)
    spigotpi(25, True, False)
    spigotpi(50, True)
    spigotpi(75, True)
    spigotpi(100, True)

if __name__ == "__main__":
    main()
