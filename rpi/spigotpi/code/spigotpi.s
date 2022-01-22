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

