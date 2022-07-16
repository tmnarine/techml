

## Assembler Implementation

The assembly for the Spigot Pi algorithm is show below.  There is learning curve to reading assembly code so I used the following to help:

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

