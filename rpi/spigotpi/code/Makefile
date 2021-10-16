
all: spigotpi

./obj/spigotpi.o: spigotpi.s
	mkdir -p bin obj
	as -g -mfpu=vfpv2 -o $@ $<

spigotpi: ./obj/spigotpi.o
	gcc -o ./bin/$@ $+

clean:
	rm ./bin/spigotpi ./obj/*.o
	
run: all
	./bin/run
