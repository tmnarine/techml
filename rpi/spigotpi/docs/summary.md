
A close reading of the assembly code will show that operations such as ```add``` always happen within a register.  The ARM architecture is referred to as ```load and store``` where values must be loaded into registers before operations can be run.

Other operations of interest to look at include saving and restoring registers and initializing variables.

To save a register's state, call ```push { arg0 }``` and later restore with ```pop { arg0 }```.

Updating a variable in memory will use registers in the following way:

```
        @ nines = 0 predigit = 0
        mov r1, #0          @ Zero value stored in register r1
        ldr r0, =nines      @ Load the address of the nines variable
        str r1, [r0]        @ Store r1 into the nines address
        ldr r0, =predigit   @ Load the address of the predigit variable
        str r1, [r0]        @ Store r1 into the predigit variable
```

## Building and Running

The GNU tools are used to build the assembly application:

```
all: spigotpi

./obj/spigotpi.o: spigotpi.s
        mkdir -p bin obj
        as -g -mfpu=vfpv2 -o $@ $<

spigotpi: ./obj/spigotpi.o
        gcc -o ./bin/$@ $+
```

Place this text into a Makefile in the same directory as ```spigotpi.s``` and run: ```make```

To run the application use: ```./bin/spigotpi```

### Note
I was not sure what to expect regarding machine stability when coding in assembly.  I am happy to report though that the Raspberry Pi has handled my programming errors such as endless loops gracefully. There seems to be no difference compared to working with regular programming language.

## Summary

It is safe to say that implementing the Spigot Pi algorithm in C or C++ would produce much better assembly code than the hand written implementation provided above.  It is often the case though, that the journey is the reward.  New and experienced developers can learn a great deal about how the Raspberry Pi operates by taking the step up to writing code in assembly.  It will not be best in all cases but learning assembly provides a good understanding of the low level operations of the Raspberry Pi. Having this knowledge as a part of your toolset can greatly assist your debugging skills. Developers often encounter issues where the high level source code is not available and must rely on the low level to figure out what has gone wrong.

