# Finding Pi using Assembler on the Rasperberry Pi


## Python Implementation

```Python
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
```

## Learning the basics of Assembler


```
@ Learning Rasberry Pi assembler

@ Rasberry Pi Assembler reference:
@   https://personal.utdallas.edu/~pervin/RPiA/RPiA.pdf

@ Data section - variables, strings etc
.data

saluation: .asciz "Learn ARM assembler"

.balign 4
intfmt: .asciz "%d"

.balign 4
intcommafmt: .asciz "%d,"

.balign 4
crmsg: .asciz "\n"

.balign 4
blankmsg: .asciz ""

.balign 4
number: .word 32

.balign 4
Array: .skip 400

@ Text section - code
.text

@ Functions have 3 parts:
@ - Save the return address: push { lr }
@ - body implementation
@ - Restore the return address and branch to it: pop { lr } and bl lr

@ r#i indicates an input
@ r#o indicates and output

print_str_r0i:
    push { lr }
    @ body
    bl puts
    pop { lr }
    bx lr
    
print_int_r0i_r1i:
    push { lr }
    @ body
    bl printf
    pop { lr }
    bx lr
    
print_int_cr_r0i_r1i:
    push { lr }
    @ body
    bl printf
    ldr r0, =blankmsg
    bl puts
    pop { lr }
    bx lr
 
print_int_array_r0i_r1i:
    push { lr }
    @ body
    mov r2, #0
    print_loop:
        cmp r2, r1
        bgt end_print_loop
        push { r0, r1, r2 }
        ldr r1, [r0, +r2, LSL #2]
        ldr r0, =intcommafmt
        bl printf
        pop { r0, r1, r2 }
        add r2, #1
        b print_loop
    end_print_loop:
    pop { lr }
    bx lr
        
multiply_by_10_r0i:
    push { lr }
    @ body
    add r1, r0, LSL #3 
    add r1, r0, LSL #1
    pop { lr }
    bx lr
    
divmod_r0i_r1i_r0o_r2o:
    push { lr }
    @ body
    mov r2, #0
    loop:
        cmp r0, r1
        blt end
        sub r0, r1
        add r2, #1
        b loop
    end:
    pop { lr }
    bx lr
    
.global main
main:
    @ Store the address we were called from
    push { lr }

    @ body implementation
    
    @ Print a string
    ldr r0, =saluation
    bl print_str_r0i
    
    @ Print a number and string
    ldr r0, =intfmt
    @ Load the data address of number first
    ldr r1, =number
    @ Then load the number from the data address
    ldr r1, [r1]
    bl print_int_cr_r0i_r1i
    
    @ Muliply 5*10
    mov r0, #5
    bl multiply_by_10_r0i
    ldr r0, =intfmt
    bl print_int_cr_r0i_r1i
    
    @ Find the mod of 11/2
    mov r0, #11
    mov r1, #2
    bl divmod_r0i_r1i_r0o_r2o
    mov r1, r0
    ldr r0, =intfmt
    bl print_int_cr_r0i_r1i
    
    @ Find the div of 11/2
    mov r0, #11
    mov r1, #2
    bl divmod_r0i_r1i_r0o_r2o
    mov r1, r2
    ldr r0, =intfmt
    bl print_int_cr_r0i_r1i
    
    @ Set data Array to all 2s
    mov r0, #0
    ldr r1, =Array
    array_loop:
        cmp r0, #100
        bgt array_end
        mov r2, #2
        @ Address r1+4*r0 = r2
        str r2, [r1, +r0, LSL #2]
        add r0, #1
        b array_loop
    array_end:

    @ Set #0 to #1 to print array
    mov r0, #0
    cmp r0, #0
    beq skip_print
    ldr r0, =Array
    mov r1, #100
    bl print_int_array_r0i_r1i
    ldr r0, =blankmsg
    bl puts
    skip_print:
    
    @ Return to the address we were called from
    pop { lr }
    bx lr
    

@ External functions
.global puts				@ C 
.global printf				@ C

@ Run: ./bin/learn
@ Output:
@ Learn ARM assembler
@ 32
@ 50
@ 1
@ 5

@ If you print the array you also get:
@ 2,2,2,2,.....

```

## Assembler Implementation

```
@ Convert the spigotpi.py Python code to Rasberry Pi assembler

@ Symbolic names for registers to aid readability
FMT .req r0
PARAM0 .req r0
PARAM1 .req r1
PARAM2 .req r2

@ Symbolic names for constants
.set N, 25
.set Alen, 1024

@ External functions
.global puts				@ C 
.global printf				@ C

@ Data section - variables, strings etc
.data

saluation: .asciz "Find PI using an integer based method:"

nStr:  .asciz "N:"

errStr: .asciz "Exit on error"

.balign 4
intFmt: .asciz "%d"

.balign 4
intCrFmt: .asciz "%d\n"

.balign 4
intCommandFmt: .asciz "%d,"

.balign 4
strIntFmt: .asciz "%s %d\n"

.balign 4
crMsg: .asciz "\n"

.balign 4
blankMsg: .asciz ""

.balign 4
A: .skip 4096 @ Array of Alen floats

@ Text section - code
.text

printStr_FMTi:
    push { lr }
    @ body
    bl puts
    pop { lr }
    bx lr
 
printStr_FMTi_PARAM1i_PARAM2i:
    push { lr }
    @ body
    bl printf
    pop { lr }
    bx lr   
    
    
multiply_by_10_PARAM0i_PARAM1o:
    push { lr }
    @ body
    add PARAM1, PARAM0, LSL #3 
    add PARAM1, PARAM0, LSL #1
    pop { lr }
    bx lr
    
divmod_PARAM0i_PARAM1i_PARAM0o_PARAM2o:
    push { lr }
    @ body
    mov PARAM2, #0
    loop:
        cmp PARAM0, PARAM1
        blt end
        sub PARAM0, PARAM1
        add PARAM2, #1
        b loop
    end:
    pop { lr }
    bx lr

.global main
.func main

main:
   @ Store the address we were called from
    push { lr }
    
    @ Salutation
    ldr FMT, =saluation
    bl printStr_FMTi
    
    @ Output N
    ldr FMT, =strIntFmt
    ldr PARAM1, =nStr
    mov PARAM2, #N
    bl printStr_FMTi_PARAM1i_PARAM2i
    
    @ Check N is >= 1
    mov r0, #N
    cmp r0, #1
    bge VALID_N
    ldr FMT, =errStr
    bl printStr_FMTi
	b END_MAIN
    
    VALID_N:
    
    @ LEN = math.floor(10 * N / 3) + 1
    mov PARAM0, #N
    mov PARAM1, #3
    bl divmod_PARAM0i_PARAM1i_PARAM0o_PARAM2o
    mov PARAM0, PARAM2
    bl multiply_by_10_PARAM0i_PARAM1o
    add PARAM1, #1
    
    ldr FMT, =intCrFmt
	bl printStr_FMTi_PARAM1i_PARAM2i
	
	@ Check LEN (PARAM1) is < Alen
    mov r0, PARAM1
    cmp r0, #Alen
    blt VALID_ALEN
    ldr FMT, =errStr
    bl printStr_FMTi
	b END_MAIN
	
	VALID_ALEN:
	
	
	
	END_MAIN:

	@ Reset r0 for no error code
    mov r0, #0
	
    @ Return to the address we were called from
    pop { lr }
    bx lr

```

## Summary


