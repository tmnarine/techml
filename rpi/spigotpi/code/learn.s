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

