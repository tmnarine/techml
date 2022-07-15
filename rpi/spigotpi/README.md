# Finding Pi using Assembler

As a software developer, I normally program in one of C++, Objective-C, Python or Swift.  Programming in assembler has been out of reach and over the years I only learned the very basics of reading assembly language. 

For the new and upcoming developers that may be reading this, assembly code is a low level language that describes the operations to be executed on a central processing unit(CPU).  Compared to programming in a language like Python, you are no longer working with variables or arrays.  Instead you are working with CPU registers and memory and knowledge of low level computing operations becomes important.

After buying my Raspberry Pi about a year ago, I decided to make learning assembly one of my pandemic goals.  With various shutdowns in my part of the world I decided to follow through on my goal.  The Raspberry Pi makes learning assembly very easy as the standard GNU toolchain is available including the GNU assembler(GAS) along with an abundant supply of reference documentation on the web.

Now all I had to do was decide on a project.  I had heard about integer methods for calculating the number Pi and I looked this up on the web.  I thought that using integer math would be a good place to start as it avoids the complications of floating point operations. The specific method I came across is called the Spigot Pi calculation.

## Approach

It would have been very difficult to write the assembly code as a first step.  Instead I took multiple steps to get to the final result:

- Implement the Spigot Pi algorithm in Python
- Add low level operations to the Python code that would mimick assembly instructions.  For example, implementing division with a loop
- Write my first assembly program to implement some of the functions that I will need for the final program.  For example, printing, div/mod math operations, initializing an array
- Finally, implement the Spigot Pi algorithm in assembly using all that I have learned in the previous steps

A divide an conquer approach was taken to write the final assembly code.


## Python Implementation

The Python code is shown below and it is the product of steps 1 and 2 described above.  The initial Python code implementation follows the Pascal code found in the document link at the top of the source code.  I won't mention a lot about the initial implementation but instead will focus on the updates I made that got me closer to writing the assembly code.  I used several programming techniques to improve code readability and result verification. Code **closures** implementing the low level operations and **assertions** to verify the result will be described next.

### Closures and Low level operations

For new software developers, a closure can be described as a function within a function.  The inner function inherits the state of the parent such as variables.  This programming technique can be used to hide functionality from outside scopes of code.

Here is a closure example:

```Python
def spigotpi(N, printResult, debugInfo = False):

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
```

The ```calcLen()``` function is embedded within ```spigotpi``` and it inherits the ```use_lowlevel``` variable.  Although closures are not really needed for the Python implementation, I chose to write the code this way so that the function implementation is located next to where it is called from.

The closure functions were used to handle the normal Python operations or the Low level operations which mimick the assembly language based on the ```use_lowlevel``` variable.

An example of a low level operation is multiplying by 10 using left shifts such as:
```u = (N << 3) + (N << 1)```.

Note that above, I multiplied ```N``` by 10 before dividing by 3 so that I could avoid floating point math.

This low level closure pattern repeats itself through the Python code.

### Assertions

Asserting is a technique where a programmer can quickly see if the code is producing the right answer.  In the following ```for``` loop we check to make sure our result matches the well known Pi value that is available on the web.

```Python
    for i in range(0, check_len-1):
        assert(pi_str[i] == spigotpi_str[i+1])
```


If the strings did not match, the assert would generate an error to let us know the algorithm failed.  Using assertions is something I take advantage of in my daily programming as it helps to check current and future changes to the code.


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
    
    print("N: ", N)
    print("LEN: ",LEN)
    
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
            
            print(" A[i-1] ",A[i-1]," ",end="")
            
            x = calcX()
            A[i-1] = calcPreviousA()
            q = calcQ()
            
            print(j,i,end="")
            print(" x",x,end="")
            print(" A[i-1]",A[i-1],end="")
            print(" q",q)

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
        
        print("A[0]",A[0],end="")
        print(" q",q)

        # import pdb; pdb.set_trace()
        
        if True:
            print("nines: ",nines,"predigit: ",predigit,end="")
            if 9 == q:
                nines += 1
                print("")
            else:
                newdigit = predigit+1 if 10 == q else predigit
                spigotpi_str += ("%d" % (newdigit))
                print(" newdigit: ",newdigit," ")
                newdigit = 0 if 10 == q else 9
                for k in range(0, nines):
                    spigotpi_str += ("%d" % (newdigit))
                predigit = 0 if 10 == q else q
                if 10 != q:
                    nines = 0
            print("nines: ",nines,"predigit: ",predigit)
        else:
            print("j: ",j,"q: ",q,"nines: ",nines,"predigit: ",predigit)
            if 9 == q:
                nines += 1
                print("") 
            else:
                predigit = 0 if 10 == q else q
                if 10 != q:
                    nines = 0
            print("j: ",j,"q: ",q,"nines: ",nines,"predigit: ",predigit)

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
    spigotpi(15, True, False)
    return
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


## Learning the basics of Assembler Programming

Assembly programming is very low level as you are working with registers, stacks, bits and flags to name a few things.  There is a fair bit of extras you need to handle yourself.  For example, you must keep track of the location a function is called from and reset that in a register when you are ready to return to that location.  Additionally, there are a limited number of registers in assembly and these must be managed throughout the code.

Assembly code can do many things such as:

- Call existing C functions such as ```puts``` and ```printf```
- Calculate using ```add``` and ```subtract```
- Reference strings and data arrays

In the ```learn.s``` module shown below, there are implementations of simple operations needed for the final Spigot Pi assembly code.  The code is divided into two parts:

- .data : contains the strings and memory used for the application
- .text : contains the assembly code including functions

The most important function in the .text section is main as this is where the code starts running from.

The reference found at the top of the source code is a good place to start learning how to program assembly on Rasberry Pi. In addition, there are some helpful comments within the code.

```
@ Learning Rasberry Pi assembler

@ Rasberry Pi Assembler reference:
@   https://personal.utdallas.edu/~pervin/RPiA/RPiA.pdf

@ Data section - variables, strings etc
.data

@ Symbolic names for constants
.set PRINT_ARRAY, 1          @ Print A array is non zero
.set ELEM_ARRAY, 33        @ Defaut element value of A array

saluation: .asciz "Learn ARM 32 bit assembler"

.balign 4
intFmt: .asciz "%d"

.balign 4
intCommaFmt: .asciz "%d,"

.balign 4
crMsg: .asciz "\n"

.balign 4
blankMsg: .asciz ""

.balign 4
number: .word 32

.balign 4
Array: .skip 400

@ Text section - code
.text

@ Functions have 3 parts:
@ - Save the return address: push { lr }
@ - Body implementation
@ - Restore the return address and branch to it: pop { lr } and bx lr

@ Args: 
@   string : arg0
@
printStr:      @ Put a string
    push { lr }
        @ body
        bl puts
    pop { lr }
    bx lr
    
@ Args:
@   string format : arg0
@   required types that match format string : arg1, arg2, ... 
@
printStrWithArgs:  @ Printf: format r0, arg ar1
    push { lr }
        @ body
        bl printf
    pop { lr }
    bx lr
    
@ Args:
@   string format : arg0
@   required types that match format string : arg1, arg2, ... 
@
printStrLineWithArgs: @Printf with \n: format r0, arg ar1
    push { lr }
        @ body
        bl printf
        ldr r0, =blankMsg
        bl puts
    pop { lr }
    bx lr
 
@ Args:
@   int array : arg0
@   int : arg1 array length
@
printIntArray: @ Printf int array: array r0, size r1
    push { lr }
        @ body
        mov r2, #0
        print_loop:
            cmp r2, r1
            bgt end_print_loop
            push { r0, r1, r2 }
            ldr r1, [r0, +r2, LSL #2]
            ldr r0, =intCommaFmt
            bl printf
            pop { r0, r1, r2 }
            add r2, #1
            b print_loop
        end_print_loop:
    pop { lr }
    bx lr
        
@ Args:
@   int : arg0 
@   int : arg1 result
@
multiplyBy10: @ Multiply r0 by 10, return result in r1
    push { lr }
        @ body
        add r1, r0, LSL #3 
        add r1, r0, LSL #1
    pop { lr }
    bx lr
    
@ Args:
@   int : arg0 number
@   int : arg1 divisor
@   int : arg2 division result
@   int : arg0 modulus result
@
findDivMod: @ Divide r0/r1, return remainer in r0
    push { lr }         @ and result in r2
        @ body
        mov r2, #0
        loop:               @ Loop start label
            cmp r0, r1
            blt end
            sub r0, r1
            add r2, #1
            b loop          @ Branch to label
        end:                @ Loop end label
    pop { lr }
    bx lr
  
@ Code that calls the subroutines
.global main
main:
    @ Store the address we were called from
    push { lr }

        @ body implementation
        
        @ Print a string
        ldr r0, =saluation
        bl printStr
        
        @ Print a number and string
        ldr r0, =intFmt
        @ Load the data address of number first
        ldr r1, =number
        @ Then load the number from the data address
        ldr r1, [r1]
        bl printStrLineWithArgs
        
        @ Multiply 5*10
        mov r0, #5
        bl multiplyBy10
        ldr r0, =intFmt
        bl printStrLineWithArgs
        
        @ Find the mod of 11/2
        mov r0, #11
        mov r1, #2
        bl findDivMod
        mov r1, r0
        ldr r0, =intFmt
        bl printStrLineWithArgs
        
        @ Find the div of 11/2
        mov r0, #11
        mov r1, #2
        bl findDivMod
        mov r1, r2
        ldr r0, =intFmt
        bl printStrLineWithArgs
        
        @ Set data Array to a default value
        mov r0, #0
        ldr r1, =Array
        array_loop:
            cmp r0, #100
            bgt array_end
            mov r2, #ELEM_ARRAY
            @ Address r1+4*r0 = r2
            str r2, [r1, +r0, LSL #2]
            add r0, #1
            b array_loop
        array_end:

        @ Set #0 to #1 to print array
        mov r0, #PRINT_ARRAY
        cmp r0, #0
        beq skip_print
        ldr r0, =Array
        mov r1, #100
        bl printIntArray
        ldr r0, =blankMsg
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
@ 33,33,33,33,33,.....

```


## Assembler Implementation

The assembly for the Spigot Pi algoritm is show below.  There is learning curve to reading assembly code so I used the following to help:

- Symbolic names for registers : PARAM0 .req r0
- Symbolic names for constants : .set N, 25

Calling a function involves setting the parameters and then branching:

```
        @ LEN = math.floor(10 * N / 3) + 1
        mov arg0, #N
        mov arg1, #3
        bl findDivMod
        mov arg0, arg2
        bl multiplyBy10
```

Looping is also required in the algorithm and labels are placed in the code to set start and end addresses:

```
        mov j, #0
        
      START_LOOP_J:
        mov r0, #N
        add r0, #1
        cmp j, r0
        beq END_LOOP_J

        @ Loop code
        
      END_LOOP_J:
```

Print debugging is supported in the assembler with some simple constructs.  We define a debug control constant:

```
.set DBG, 1         @ Emit debug info if set
```

The debug constant is tested to see the print information code should be run:

```
        mov r0, #DBG
        cmp r0, #0
        beq DBG2
        mov r0, r1
        mov r1, len  
        bl printIntArray
      DBG2:
```

Comments are interspersed in the assembly code to help the reader.

```
@ Convert the spigotpi.py Python code to Rasberry Pi assembler

@ Symbolic names for registers to aid readability
arg0 .req r0
arg1 .req r1
arg2 .req r2
arg3 .req r3
arg4 .req r4
arg5 .req r5


@ Symbolic names for constants
.set N, 45          @ Number of digits of PI to find
.set A_LEN, 1024    @ Number of float elements in A
.set DBG, 0         @ Emit debug info if set

@ External functions
.global puts                @ C 
.global printf              @ C

@ Data section - variables, strings etc. that allow modification
.data

saluation: .asciz "Find Pi on Raspberry Pi using an integer based method in ARM 32 bit assembler:"

nStr:  .asciz "N:"

lenStr:  .asciz "LEN:"

xStr:  .asciz " x"

qStr:  .asciz " q"

aPrevStr: .asciz " A[i-1]"

aZeroStr: .asciz "A[0]"

ninesStr: .asciz "nines:"

predigitStr: .asciz "predigit:"

errStr: .asciz "Exit on error"

.balign 4
intFmt: .asciz "%d"

.balign 4
intCrFmt: .asciz "%d\n"

.balign 4
intsCrFmt: .asciz "%d %d\n"

.balign 4
intsFmt: .asciz "%d %d "

.balign 4
intCommaFmt: .asciz "%d,"

.balign 4
strIntFmt: .asciz "%s %d\n"

.balign 4
strIntFmt2: .asciz "%s %d "

.balign 4
crMsg: .asciz "\n"

.balign 4
blankMsg: .asciz ""

.balign 4
A: .skip 4096 @ float A[ALENGTH]

.balign 4
predigit: .word 32

.balign 4
nines: .word 32

@ Text section or code (no modifications allowed)
.text

@ Args: 
@   string : arg0
@
printStr:
    push { lr }
        @ body
        bl puts
    pop { lr }
    bx lr
 
@ Args:
@   string format : arg0
@   required types that match format string : arg1, arg2, ... 
@
printStrWithArgs:
    push { lr }
        @ body
        bl printf
    pop { lr }
    bx lr   
    
@ Args:
@   int : arg0
@   int : arg1 result
@
multiplyBy10:
    push { lr }
        @ body
        mov arg1, #0
        add arg1, arg0, LSL #3 
        add arg1, arg0, LSL #1
    pop { lr }
    bx lr
  
@ Args:
@   int : arg0 a
@   int : arg1 b
@   int : arg2 c = a * b
@
multiplyBy:
    push { lr }
        @ body
        push { arg1 }
        mov arg2, #0
        loopMultiplyBy:
            cmp arg1, #0
            beq endMultiplyBy
            add arg2, arg0
            sub arg1, #1
            b loopMultiplyBy
        endMultiplyBy:
        pop { arg1 }
    pop { lr }
    bx lr
 
@ Args:
@   int : arg0 number
@   int : arg1 divisor
@   int : arg2 division result
@   int : arg0 modulus result
@
findDivMod:
    push { lr }
        @ body
        mov arg2, #0
        loop:
            cmp arg0, arg1
            blt end
            sub arg0, arg1
            add arg2, #1
            b loop
        end:
    pop { lr }
    bx lr

@ Args:
@   int array : arg0
@   int : arg1 array length
@
printIntArray:
    push { lr }
        @ body
        mov r2, #0
        print_loop:
            cmp r2, r1
            bgt end_print_loop
            push { r0, r1, r2 }
            ldr r1, [r0, +r2, LSL #2]
            ldr r0, =intCommaFmt
            bl printf
            pop { r0, r1, r2 }
            add r2, #1
            b print_loop
        end_print_loop:
        ldr arg0, =blankMsg
        bl printStr
    pop { lr }
    bx lr
    
    
.global main
.func main
main:
   @ Store the address we were called from
    push { lr }
    
        @ Salutation
        ldr arg0, =saluation
        bl printStr
        
        @ Output N
        ldr arg0, =strIntFmt
        ldr arg1, =nStr
        mov arg2, #N
        bl printStrWithArgs
        
        @ Check N is >= 1
        mov r0, #N
        cmp r0, #1
        bge VALID_N			@ Branch of >= 1
        ldr arg0, =errStr	@ Else display error and go to end of main
        bl printStr
        b END_MAIN
        
      VALID_N:
        
        @ LEN = math.floor(10 * N / 3) + 1
        mov arg0, #N
        bl multiplyBy10 @ Output in arg1
        mov arg0, arg1
        mov arg1, #3
        bl findDivMod
        mov arg0, arg2
        add arg0, #1
        
        @ Output LEN
        push { arg0 }
        mov arg2, arg0
        ldr arg0, =strIntFmt
        ldr arg1, =lenStr
        bl printStrWithArgs
        pop { arg0 }

        @ Make alias for registers we will use multiple times
        len .req r5
        j   .req r6
        i   .req r7
        n   .req r8
        q   .req r9
        x   .req r10

        @ Store LEN in its own register
        mov len, arg0
        
        mov r0, #DBG
        cmp r0, #0
        beq DBG1
        push { arg1 }
        ldr arg0, =intCrFmt
        bl printStrWithArgs
        pop { arg1 }
      DBG1:

        @ Check LEN (arg1) is < A_LEN
        mov r0, arg1
        cmp r0, #A_LEN
        blt VALID_A_LEN
        ldr arg0, =errStr
        bl printStr
        b END_MAIN

      VALID_A_LEN:
              
        @ Set array A[0..LEN] to 2s
        mov i, #0
        ldr r1, =A
        ARRAY_LOOP:
            cmp i, len
            bgt ARRAY_END
            mov r2, #2
            @ Address r1+4*i = r2
            str r2, [r1, +i, LSL #2]
            add i, #1
            b ARRAY_LOOP
        ARRAY_END:  
        
        mov r0, #DBG
        cmp r0, #0
        beq DBG2
        mov r0, r1
        mov r1, len  
        bl printIntArray
      DBG2:
              
        @ nines = 0 predigit = 0
        mov r1, #0
        ldr r0, =nines
        str r1, [r0]
        ldr r0, =predigit
        str r1, [r0]
        
        mov j, #1
        
      START_LOOP_J:
        mov r0, #N
        add r0, #1
        cmp j, r0
        beq END_LOOP_J
        
        @ q = 0 i = len
        mov q, #0
        mov i, len
           
      START_LOOP_I:
        cmp i, #0
        beq END_LOOP_I

        mov r0, #DBG
        cmp r0, #0
        beq DBG3
        @ Output A[i-1]
        ldr arg0, =A
        mov r1, i
        sub r1, #1
        ldr arg0, [arg0, +r1, LSL#2]
        mov arg2, arg0
        ldr arg0, =strIntFmt2
        ldr arg1, =aPrevStr
        bl printStrWithArgs
                
        @ j, i
        ldr r0, =intsFmt
        mov r1, j
        mov r2, i
        bl printStrWithArgs
      DBG3:
        
        @ x = (10 * A[i-1] + q * i)
        ldr arg0, =A
        mov r1, i
        sub r1, #1
        ldr arg0, [arg0, +r1, LSL#2]
        bl multiplyBy10
        
        mov x, arg1
        mov arg0, q
        mov arg1, i
        bl multiplyBy
        add x, arg2
        
        mov r0, #DBG
        cmp r0, #0
        beq DBG4
        @ Output x
        ldr arg0, =strIntFmt2
        ldr arg1, =xStr
        mov arg2, x
        bl printStrWithArgs
      DBG4:
        
        @ A[i-1] = (x % (2 * i - 1))
        mov arg1, i, LSL#1
        sub arg1, #1
        mov arg0, x
        bl findDivMod @ modulus returned in arg0
        ldr r1, =A
        mov r2, i
        sub r2, #1
        str arg0, [r1, +r2, LSL #2]
        
        mov r0, #DBG
        cmp r0, #0
        beq DBG5
        @ Output A[i-1]
        mov arg2, arg0
        ldr arg0, =strIntFmt2
        ldr arg1, =aPrevStr
        bl printStrWithArgs
      DBG5:
        
        @ q = ( x / (2 * i -1))
        mov arg1, i, LSL#1
        sub arg1, #1
        mov arg0, x
        bl findDivMod @ result returned in arg2
        mov q, arg2
        
        mov r0, #DBG
        cmp r0, #0
        beq DBG6
        @ Output q
        mov arg2, q
        ldr arg0, =strIntFmt
        ldr arg1, =qStr
        bl printStrWithArgs
      DBG6:
        
        @ i = i - 1
        sub i, #1
        
        b START_LOOP_I
        
      END_LOOP_I:
      
        @ A[0] = (q % 10)
        mov arg0, q
        mov arg1, #10
        bl findDivMod @ modulus returned in arg0
        ldr r3, =A
        mov r4, #0
        str arg0, [r3, +r4, LSL #2]
        
        @ q = (q / 10)
        @ arg2 preserved still from findDivMod call
        mov q, arg2
        
        mov r0, #DBG
        cmp r0, #0
        beq DBG7
        @ Output A[0]
        mov arg2, arg0
        ldr arg0, =strIntFmt2
        ldr arg1, =aZeroStr
        bl printStrWithArgs
        
        @ Output q
        mov arg2, q
        ldr arg0, =strIntFmt
        ldr arg1, =qStr
        bl printStrWithArgs
       DBG7:

        @ Output code
         
        mov r0, #DBG
        cmp r0, #0
        beq DBG8
        ldr arg0, =strIntFmt2
        ldr arg1, =ninesStr
        ldr arg2, =nines
        ldr arg2, [arg2]
        bl printStrWithArgs
        
        ldr arg0, =strIntFmt
        ldr arg1, =predigitStr
        ldr arg2, =predigit
        ldr arg2, [arg2]
        bl printStrWithArgs
       DBG8:

        @ if 9 == q: nines += 1
        cmp q, #9
        bne Q_NOT_EQUAL_9
        ldr r0, =nines
        ldr r0, [r0]
        add r0, #1
        ldr r1, =nines
        str r0, [r1]
        b OVER_ELSE
      Q_NOT_EQUAL_9:
      
        @ else
        @ newdigit = predigit+1 if 10 == q else predigit
        ldr r1, =predigit
        ldr r1, [r1]
        cmp q, #10
        bne Q_NOT_EQUAL_TO_10
        add r1, #1
      Q_NOT_EQUAL_TO_10:
      
        @ spigotpi_str += ("%d" % (newdigit))
        ldr r0, =intFmt
        bl printStrWithArgs
        
        @ newdigit = 0 if 10 == q else 9
        mov r1, #0
        cmp q, #10
        beq Q_NOT_EQUAL_TO__10
        mov r1, #9
        ldr r3, =predigit
        str r1, [r3]
      Q_NOT_EQUAL_TO__10:
        
        @ for k in range(0, nines): spigotpi_str += ("%d" % (newdigit))
        ldr r3, =nines
        ldr r3, [r3]
        mov r4, #0
      K_LOOP_START:
        cmp r4, r3
        beq K_LOOP_DONE
        push { r3 }
        ldr r0, =intFmt
        bl printStrWithArgs @ r1/predigit already set
        add r4, #1
        pop { r3 }
        b K_LOOP_START
      K_LOOP_DONE:

        @ predigit = 0 if 10 == q else q
        mov r0, #0
        cmp q, #10
        beq Q_EQUALS_10
        mov r0, q
      Q_EQUALS_10:
        ldr r1, =predigit
        str r0, [r1]
        
        @ if 10 != q: nines = 0
        mov r0, #0
        cmp q, #10
        beq Q_EQUALS__10
        ldr r1, =nines
        str r0, [r1]
      Q_EQUALS__10:
      
      OVER_ELSE:
      
        mov r0, #DBG
        cmp r0, #0
        beq DBG9
        ldr arg0, =strIntFmt2
        ldr arg1, =ninesStr
        ldr arg2, =nines
        ldr arg2, [arg2]
        bl printStrWithArgs
        
        ldr arg0, =strIntFmt
        ldr arg1, =predigitStr
        ldr arg2, =predigit
        ldr arg2, [arg2]
        bl printStrWithArgs
       DBG9:
           
        add j, #1
        b START_LOOP_J
        
      END_LOOP_J:
      
        ldr r0, =intCrFmt
        ldr r1, =predigit
        ldr r1, [r1]
        bl printStrWithArgs
      
    END_MAIN:

    @ Reset r0 for no error code
    mov r0, #0

    @ Return to the address we were called from
    pop { lr }
    bx lr

```


## Building and Running

The GNU tools are used to build the assembly application:

```
all: spigotpi

./obj/spigotpi.o: spigotpi.s
        mkdir -p bin obj
        as -g -mfpu=vfpv2 -o $@ $<

spigotpi: ./obj/spigotpi.o
        gcc -o ./bin/$@ $+
```

Place this text into a Makefile in the same directory as ```spigotpi.s``` and run: ```make```

To run the application use: ```./bin/spigotpi```

### Note
I was not sure what to expect regarding machine stability when coding in assembly.  I am happy to report though that the Raspberry Pi has handled my programming errors such as endless loops gracefully. There seems to be no difference compared to working with regular programming language.

## Summary

It is safe to say that implementing the Spigot Pi algorithm in C or C++ would produce much better assembly code than the hand written implementation provided.  It is often though that the journey is the reward.  New and experienced developers can learn a great deal about how the Raspberry Pi operates by taking the plunge and writing code in assembly.  It will not be best in all cases but learning assembly provides a good understanding of the low level operations of the Raspberry Pi. Having this knowledge as a part of your toolset can greatly assist your debugging  when you encounter issues where the high level source code being executed is not available.

