#
# spigotpi.py -- generate pi using the spigot algorithm
#
# http://www.cs.ox.ac.uk/jeremy.gibbons/publications/spigot.pdf
# http://www.cut-the-knot.org/Curriculum/Algorithms/SpigotForPi.shtml
#

import math


def pi_as_str():
    return "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"


def spigotpi(N, printResult):
    print("Spigotpi N = %d" % N)

    LEN = math.floor(10 * N / 3) + 1
    A = [2 for i in range(0,LEN)]
    
    nines = 0
    predigit = 0

    spigotpi_str = ""

    for j in range(1, N+1):
        q = 0
        for i in range(LEN, 0, -1):
            x = 10 * A[i-1] + q * i
            A[i-1] = x % (2 * i - 1)
            q = int(x / (2 * i -1))

        A[0] = q % 10
        q = int(q / 10)

        if 9 == q:
            nines += 1
        elif 10 == q:
            spigotpi_str += ("%d" % (predigit+1))
            for k in range(0, nines):
                spigotpi_str += ("%d" % (0))
            predigit = 0
            nines = 0
        else:
            spigotpi_str += ("%d" % (predigit))
            predigit = q
            if 0 != nines:
                for k in range(0, nines):
                    spigotpi_str += ("%d" % (9))
                nines = 0

    spigotpi_str += ("%d" % (predigit))

    pi_str = pi_as_str().replace(".", "")

    len_spigotpi_str = len(spigotpi_str)
    len_pi_str = len(pi_str)
    
    check_len = len_spigotpi_str if len_spigotpi_str < len_pi_str else len_pi_str
    for i in range(0, check_len-1):
        if printResult:
            separator = "" if i == len(pi_str)-1 else "," 
            print(i, ":", pi_str[i], spigotpi_str[i+1], separator, end="")
        assert(pi_str[i] == spigotpi_str[i+1])

    print("")    
    
def main():
    spigotpi(25, True)
    spigotpi(50, True)
    spigotpi(100, True)

if __name__ == "__main__":
    main()
