import subprocess

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
    
    
def main():
    
    printResult = True
    
    print("# Running: ./bin/spigotpi")
    
    output = subprocess.check_output("./bin/spigotpi", shell=True)
    
    lines = output.splitlines()
        
    spigotpi_str = str(lines[-1], 'utf-8')
    
    pi_str = pi_as_str()
    
    len_spigotpi_str = len(spigotpi_str)
    len_pi_str = len(pi_str)
    
    # print(spigotpi_str)
    # print("0" + pi_str)
        
    check_len = len_spigotpi_str if len_spigotpi_str < len_pi_str else len_pi_str
    for i in range(0, check_len-1):
        assert(pi_str[i] == spigotpi_str[i+1])
        if printResult:
            print("%s" % (spigotpi_str[i+1]), end="")
            
    if printResult:
        print("")
        
    print("# Result verified")
    
    
if __name__ == "__main__":
    main()
