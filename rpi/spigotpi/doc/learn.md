

## Learning the basics of Assembler Programming

Assembly programming is very low level as you are working with registers, stacks, bits and flags to name a few things.  There is a fair bit of extras you need to handle yourself.  For example, you must keep track of the location a function is called from and reset that in a register when you are ready to return to that location.  Additionally, there are a limited number of registers in Assembly and these must be managed throughout the code.

Assembly code can do many things such as:

- Call existing C functions such as ```puts``` and ```printf```
- Calculate using ```add``` and ```subtract```
- Reference strings and data arrays

In the ```learn.s``` module shown below, there are implementations of simple operations needed for the final Spigot PI assembly code.  The code is divided into two parts:

- .data : contains the strings and memory used for the
application
- .text : contains the assembly code including functions

The most important function in the .text section is main as this is where the code starts running from.

The reference found at the top of the source code is a good place to start learning how to program assembly on Rasberry Pi. In addition, there are some helpful comments within the code.

