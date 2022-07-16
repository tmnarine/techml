@ Convert the spigotpi.py Python code to Rasberry Pi 32 bit assembler

@ Outstanding issues:
@ 1. Result is incorrect soon after the 45th digit.  Seeing an extra 0 and could be the
@ result of an incorrect loop.
@ 2. Code cleanup: arg# versus r#, output code

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

