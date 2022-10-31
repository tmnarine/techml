#
# spigotpi.py -- generate pi using the spigot algorithm
#
# http://stanleyrabinowitz.com/bibliography/spigot.pdf
# - contains Pascal version of the algorithm
#

import math

def pi_as_str():
    # See https://www.piday.org/million/
    pi = '''3.14159265358979323846264338327950288419716939937510582
09749445923078164062862089986280348253421170679821480865132823
06647093844609550582231725359408128481117450284102701938521105
55964462294895493038196442881097566593344612847564823378678316
52712019091456485669234603486104543266482133936072602491412737
24587006606315588174881520920962829254091715364367892590360011
33053054882046652138414695194151160943305727036575959195309218
61173819326117931051185480744623799627495673518857527248912279
38183011949129833673362440656643086021394946395224737190702179
86094370277053921717629317675238467481846766940513200056812714
52635608277857713427577896091736371787214684409012249534301465
49585371050792279689258923542019956112129021960864034418159813
62977477130996051870721134999999837297804995105973173281609631
85950244594553469083026425223082533446850352619311881710100031
37838752886587533208381420617177669147303598253490428755468731
15956286388235378759375195778185778053217122680661300192787661
11959092164201989380952572010654858632788659361533818279682303
01952035301852968995773622599413891249721775283479131515574857
24245415069595082953311686172785588907509838175463746493931925
50604009277016711390098488240128583616035637076601047101819429
55596198946767837449448255379774726847104047534646208046684259
06949129331367702898915210475216205696602405803815019351125338
24300355876402474964732639141992726042699227967823547816360093
41721641219924586315030286182974555706749838505494588586926995
69092721079750930295532116534498720275596023648066549911988183
47977535663698074265425278625518184175746728909777727938000816
47060016145249192173217214772350141441973568548161361157352552
13347574184946843852332390739414333454776241686251898356948556
2099219222184272550254256887671790494601653466804'''
    return pi.replace("\n","").replace(".", "")
    


def spigotpi(N, printResult, debugInfo = False):
    
    assert(N > 0)

    # lowlevel reduces the operation into smaller tasks that
    # can be replicated in assembler
    use_lowlevel = True

    def calcLen():
        if use_lowlevel:
            result = 0
            u = (N << 3) + (N << 1)
            v = 0
            while u >= 3:
                u -= 3
                v += 1
            result += v + 1
            return result
            
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

    pi_str = pi_as_str()

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
    spigotpi(256, True)

if __name__ == "__main__":
    main()
