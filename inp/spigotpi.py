#
# spigotpi.py -- generate pi using the spigot algorithm
#
# http://www.cs.ox.ac.uk/jeremy.gibbons/publications/spigot.pdf
# http://www.cut-the-knot.org/Curriculum/Algorithms/SpigotForPi.shtml
#

import math

# Available on the web
def pi_as_str():
    return "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"


def spigotpi(N, printResult):
    print("Spigotpi N = %d" % N)

    assert(N > 0)
    
    LEN = math.floor(10 * N / 3) + 1
    A = [2 for i in range(0,LEN)]
    
    nines = 0
    predigit = 0

    spigotpi_str = ""

    use_lowlevel = True

    for j in range(1, N+1):
        q = 0
        for i in range(LEN, 0, -1):

            def calcx():
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

            def calcq():
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
            
            x = calcx()
            A[i-1] = calcPreviousA()
            q = calcq()

        def calcA0():
            if use_lowlevel:
                u = q
                while u >= 10:
                    u -= 10
                return u
            
            return q % 10

        def calcq2():
            if use_lowlevel:
                result = 0
                u = q >> 1
                while u >= 5:
                    u -= 5
                    result += 1
                return result
            
            return int(q / 10);
        
        A[0] = calcA0()
        q = calcq2()

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

    spigotpi_str += ("%d" % (predigit))

    # Check the result

    pi_str = pi_as_str().replace(".", "")

    assert(N < len(pi_str))

    len_spigotpi_str = len(spigotpi_str)
    len_pi_str = len(pi_str)
    
    check_len = len_spigotpi_str if len_spigotpi_str < len_pi_str else len_pi_str
    for i in range(0, check_len-1):
        assert(pi_str[i] == spigotpi_str[i+1])
        if printResult:
            separator = "" if i == len(pi_str)-1 else "," 
            print(spigotpi_str[i+1], separator, end="")

    print("")    
    
def main():
    spigotpi(1, True)
    spigotpi(2, True)
    spigotpi(3, True)
    spigotpi(25, True)
    spigotpi(50, True)
    spigotpi(75, True)
    spigotpi(100, True)

if __name__ == "__main__":
    main()
