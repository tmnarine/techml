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
@ - Restore the return address and branch to it: pop { lr } and bx lr

@ Parameter notation used:
@ r#i indicates an input
@ r#o indicates and output

print_str_r0i:      @ Put a string
    push { lr }
    @ body
    bl puts
    pop { lr }
    bx lr
    
print_r0i_r1i:  @ Printf: format r0, arg ar1
    push { lr }
    @ body
    bl printf
    pop { lr }
    bx lr
    
print_cr_r0i_r1i: @Printf with \n: format r0, arg ar1
    push { lr }
    @ body
    bl printf
    ldr r0, =blankmsg
    bl puts
    pop { lr }
    bx lr
 
print_int_array_r0i_r1i: @ Printf int array: array r0, size r1
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
        
multiply_by_10_r0i: @ Multiply r0 by 10, return result in r1
    push { lr }
    @ body
    add r1, r0, LSL #3 
    add r1, r0, LSL #1
    pop { lr }
    bx lr
    
divmod_r0i_r1i_r0o_r2o: @ Divide r0/r1, return remained in r0
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
    bl print_str_r0i
    
    @ Print a number and string
    ldr r0, =intfmt
    @ Load the data address of number first
    ldr r1, =number
    @ Then load the number from the data address
    ldr r1, [r1]
    bl print_cr_r0i_r1i
    
    @ Muliply 5*10
    mov r0, #5
    bl multiply_by_10_r0i
    ldr r0, =intfmt
    bl print_cr_r0i_r1i
    
    @ Find the mod of 11/2
    mov r0, #11
    mov r1, #2
    bl divmod_r0i_r1i_r0o_r2o
    mov r1, r0
    ldr r0, =intfmt
    bl print_cr_r0i_r1i
    
    @ Find the div of 11/2
    mov r0, #11
    mov r1, #2
    bl divmod_r0i_r1i_r0o_r2o
    mov r1, r2
    ldr r0, =intfmt
    bl print_cr_r0i_r1i
    
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

