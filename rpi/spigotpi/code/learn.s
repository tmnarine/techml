@ Learning Rasberrypi assembler

@ Rasberrypi assembler reference: 
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
main_return: .word 0

.balign 4
func_return: .word 0

.balign 4
Array: .skip 400

@ Text section - code
.text

@ r#i indicates an input
@ r#o indicates and output

print_str_r0i:
    ldr r1, =func_return
    str lr, [r1]
    bl puts
    ldr r1, =func_return
    ldr lr, [r1]
    bx lr
    
print_int_r0i_r1i:
    ldr r2, =func_return
    str lr, [r2]
    bl printf
    ldr r2, =func_return
    ldr lr, [r2]
    bx lr
    
print_int_cr_r0i_r1i:
    ldr r2, =func_return
    str lr, [r2]
    bl printf
    ldr r0, =blankmsg
    bl puts
    ldr r2, =func_return
    ldr lr, [r2]
    bx lr
 
print_int_array_r0i_r1i:
    ldr r2, =func_return
    str lr, [r2]
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
    ldr r2, =func_return
    ldr lr, [r2]
    bx lr
        
multiply_by_10_r0i:
    ldr r2, =func_return
    str lr, [r2]
    add r1, r0, LSL #3 
    add r1, r0, LSL #1
    ldr r2, =func_return
    ldr lr, [r2]
    bx lr
    
divmod_r0i_r1i_r0o_r2o:
    ldr r3, =func_return
    str lr, [r3]
    mov r2, #0
    loop:
        cmp r0, r1
        blt end
        sub r0, r1
        add r2, #1
        b loop
    end:
    ldr r3, =func_return
    ldr lr, [r3]
    bx lr
    
.global main
main:
    @ Store the address we were called from
    ldr r1, =main_return
    str lr, [r1]
    
    @ Print a string
    ldr r0, =saluation
    bl print_str_r0i
    
    @ Print a number and string
    ldr r0, =intfmt
    ldr r1, =number
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
    
    @ Set Array to all 2s
    mov r0, #0
    ldr r1, =Array
    array_loop:
        cmp r0, #100
        bgt array_end
        mov r2, #3
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
    ldr r1, =main_return
    ldr lr, [r1]
    bx lr
    

@ External functions
.global puts				@ C 
.global printf				@ C

@ Output is running ./bin/learn is:
@ Learn ARM assembler
@ 32
@ 50
@ 1
@ 5


