# Finding Pi using Assembler

As a software developer, I normally program in one of C++, Objective-C, Python 
or Swift.  Programming in assembler has been out of reach for me and over the
years I only learned the very basics of reading assembly language. 

For the new and upcoming developers that may be reading this, assembly is a low level 
language that describes the operations to be executed on a central processing 
unit(CPU).  Compared to programming in a language like Python, you are no 
longer working with variables or arrays.  Instead you are working with CPU registers 
and memory and knowledge of bit operations becomes more important.

After buying my Raspberry Pi about a year ago, I decided to make learning
assembly one of my pandemic goals.  With various shutdowns in my part of 
the world I had time of my hands.  The Raspberry Pi makes learning
assembly very easy as the standard GNU toolchain is available including the
GNU assembler(AS) along with plenty of reference documentation on the web.

Now all I had to do was decide on a project.  I had heard about integer methods
for calculating PI and I looked this up on the web.  I thought that this 
would be a good place to start to avoid the complications of floating
point operations.  The specific method I came across is called the spigotpi
calculation.

## Process

It would have been very difficult for me to write the assembly code as a 
first step.  Instead I took multiple steps to get to the final result:

- Implement the Spigot Pi algorithm in Python
- Add low level operations to the Python code that would mimick assembly 
instructions.  For example, implementing division with a loop
- Write my first assembly program to implement some of the function
that I will need for the final program.  For example, printing, div/mod
math operations, initializing an array
- Finally, implement the Spigot Pi algorithm in assembly using all that
I have learned in the previous steps

A divide an conquer approach to wrting the final assembly code.

