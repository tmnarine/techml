@ Convert the spigotpi.py code to Rasberrypi assembler

@ Rasberrypi assembler reference: 
@   https://personal.utdallas.edu/~pervin/RPiA/RPiA.pdf

.global main
.func main

main:
	mov r0, #255
	bx lr

