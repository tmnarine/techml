
all: spigotpi learn

./obj/spigotpi.o: spigotpi.s
	mkdir -p bin obj
	as -g -mfpu=vfpv2 -o $@ $<

spigotpi: ./obj/spigotpi.o
	gcc -o ./bin/$@ $+
	
./obj/learn.o: learn.s
	mkdir -p bin obj
	as -g -mfpu=vfpv2 -o $@ $<

learn: ./obj/learn.o
	gcc -o ./bin/$@ $+
	
clean:
	rm ./bin/spigotpi ./bin/learn ./obj/*.o
	
run: all
	./bin/run
	
runlearn: all
	./bin/runlearn
