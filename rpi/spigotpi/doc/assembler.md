

## Assembler Implementation

The assembly for the Spigot PI algoritm is show below.  There is learning curve to reading assembly code so I used the following to help:

- Symbolic names for registers : PARAM0 .req r0
- Symbolic names for constants : .set N, 25

Along with explicit names for functions that include parameters, we use these such as:

```
    mov PARAM0, #N
    mov PARAM1, #3
    bl divmod_PARAM0i_PARAM1i_PARAM0o_PARAM2o
```

Looping is also required in the algorithm and labels are placed in the code:

```
    mov Jreg, #0
  START_LOOP_J:
    cmp Jreg, NPLUSONEreg
    beq END_LOOP_J
```

Comments are interspersed in the code to help the reader.

