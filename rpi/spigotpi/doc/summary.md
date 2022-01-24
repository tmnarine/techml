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

Place this text into a Makefile in the same directory as ```spigotpi.s``` and
run: ```make```

To run the application use: ```./bin/spigotpi```

### Note
I was not sure what to expect regarding machine stability when coding
in assembly.  I am happy to report though that the Raspberry Pi has 
handled my programming errors such  as endless loops gracefully. There 
seems to be no difference compared to working with regular  programming language.

## Summary

It is safe to say that implementing the Spigot Pi algorithm in C or C++ would 
produce much better code than the implementation provided.  But  the journey 
is the reward.  New and experienced developers can learn a great deal about 
how the Raspberry Pi operates by taking the plunge and writing code in 
assembler.  It will not be best in all cases but learning assembly provides 
a good understanding of the low level operations of the Pi.  

Happy Pi day!

