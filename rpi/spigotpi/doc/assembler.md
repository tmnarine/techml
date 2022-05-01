

## Assembler Implementation

The assembly for the Spigot Pi algoritm is show below.  There is learning curve to reading assembly code so I used the following to help:

- Symbolic names for registers : PARAM0 .req r0
- Symbolic names for constants : .set N, 25

Along with explicit names for functions that include parameters, we use these such as:

```
        @ LEN = math.floor(10 * N / 3) + 1
        mov arg0, #N
        mov arg1, #3
        bl findDivMod
        mov arg0, arg2
        bl multiplyBy10
```

Looping is also required in the algorithm and labels are placed in the code:

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

Comments are interspersed in the code to help the reader.

