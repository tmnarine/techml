
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
	python3 check_spigotpi_assembler.py
	
runpy: 
	python3 spigotpi.py
	
runlearn: all
	./bin/runlearn

# Build the README.md from the code and other .md files	
doc:
	mv ../README.md /var/tmp
	cat ../docs/intro.md > ../README.md
	cat ../docs/python.md >> ../README.md
	echo \`\`\`Python >> ../README.md
	cat ../code/spigotpi.py >> ../README.md
	echo \`\`\` >> ../README.md
	cat ../docs/learn.md >> ../README.md
	echo \`\`\` >> ../README.md
	cat ../code/learn.s >> ../README.md
	echo \`\`\` >> ../README.md
	cat ../docs/assembler.md >> ../README.md
	echo \`\`\` >> ../README.md
	cat ../code/spigotpi.s >> ../README.md
	echo \`\`\` >> ../README.md
	cat ../docs/summary.md >> ../README.md
