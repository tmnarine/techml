import subprocess

# Available on the web
def pi_as_str():
    return "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"

def main():
    
    printResult = True
    
    print("# Running: ./bin/spigotpi")
    
    output = subprocess.check_output("./bin/spigotpi", shell=True)
    
    lines = output.splitlines()
        
    spigotpi_str = str(lines[-1], 'utf-8')
    
    pi_str = pi_as_str().replace(".", "")
    
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
