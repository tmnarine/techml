@ Convert the spigotpi.py Python code to Rasberry Pi assembler

@ Symbolic names for registers to aid readability
FMT .req r0
PARAM0 .req r0
PARAM1 .req r1
PARAM2 .req r2
VAARG0 .req r0
VAARG1 .req r1


@ Symbolic names for constants
.set N, 25        @ Number of digits of PI to find
.set Alen, 1024   @ Number of float elements in A

@ External functions
.global puts                @ C 
.global printf              @ C

@ Data section - variables, strings etc. that allow modification
.data

saluation: .asciz "Find PI using an integer based method:"

nStr:  .asciz "N:"

errStr: .asciz "Exit on error"

.balign 4
intFmt: .asciz "%d"

.balign 4
intCrFmt: .asciz "%d\n"

.balign 4
intCommaFmt: .asciz "%d,"

.balign 4
strIntFmt: .asciz "%s %d\n"

.balign 4
crMsg: .asciz "\n"

.balign 4
blankMsg: .asciz ""

.balign 4
A: .skip 4096 @ float A[Alen]

@ Text section or code (no modifications allowed)
.text

printStr_FMTi:
    push { lr }
    @ body
    bl puts
    pop { lr }
    bx lr
 
printStr_FMTi_VAARG0i:
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

printIntArray_PARAM0i_PARAM1i:
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
    bl printStr_FMTi_VAARG0i
    
    @ Check N is >= 1
    mov r0, #N
    cmp r0, #1
    bge VALID_N			@ Branch of >= 1
    ldr FMT, =errStr	@ Else display error and go to end of main
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
    
    @push { PARAM1 }
    @ldr FMT, =intCrFmt
    @bl printStr_FMTi_PARAM1i_PARAM2i
    @pop { PARAM1 }

    @ Check LEN (PARAM1) is < Alen
    mov r0, PARAM1
    cmp r0, #Alen
    blt VALID_ALEN
    ldr FMT, =errStr
    bl printStr_FMTi
    b END_MAIN

  VALID_ALEN:
  
    @ Store LEN in R3
    mov r3, PARAM1
    
    @ Set array A[0..LEN] to 2s
    mov r0, #0
    ldr r1, =A
    ARRAY_LOOP:
        cmp r0, r3
        bgt ARRAY_END
        mov r2, #2
        @ Address r1+4*r0 = r2
        str r2, [r1, +r0, LSL #2]
        add r0, #1
        b ARRAY_LOOP
    ARRAY_END:  
    
    mov r0, r1
    mov r1, r3  
    bl printIntArray_PARAM0i_PARAM1i

    Areg .req r0
    LENreg .req r1
    NINESreg .req r3
    PREDIGITreg .req r4
    Jreg .req r5
    Ireg .req r6
    Qreg .req r7
    Xreg .req r8
    APREVreg .req r9
    NPLUSONEreg .req r10
    
    mov NPLUSONEreg, #N
    add NPLUSONEreg, #1
    
    mov Jreg, #0
  START_LOOP_J:
    cmp Jreg, NPLUSONEreg
    beq END_LOOP_J
    
    mov Qreg, #0
    
    mov Ireg, LENreg
  START_LOOP_I:
    cmp Ireg, #-1
    beq END_LOOP_I
    
    
    sub Ireg, #1
    
    b START_LOOP_I
    
  END_LOOP_I:
    
    add Jreg, #1
    b START_LOOP_J
    
  END_LOOP_J :   
       

  END_MAIN:

    @ Reset r0 for no error code
    mov r0, #0

    @ Return to the address we were called from
    pop { lr }
    bx lr

