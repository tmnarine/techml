

## Python Implementation

The Python code is shown below and it is the product of steps 1 and 2 described above.  The initial Python code implementation follows the Pascal code found in the document link at the top of the source code.  I won't mention a lot about the initial implementation but instead will focus on the updates I made that got me closer to writing the assembly code.  I used several programming techniques to improve code readability and result verification. Code **closures** implementing the low level operations and **assertions** to verify the result will be described next.

### Closures and Low level operations

For new software developers, a closure can be described as a function within a function.  The inner function inherits the state of the parent such as variables.  This programming technique can be used to hide functionality from outside scopes of code.

Here is a closure example:

```Python
def spigotpi(N, printResult, debugInfo = False):

    use_lowlevel = True

    def calcLen():
        if use_lowlevel:
            result = 0
            u = (N << 3) + (N << 1)
            v = 0
            while u >= 3:
                u -= 3
                v += 1
            result += v + 1
            return result

        return math.floor(10 * N / 3) + 1
```

The ```calcLen()``` function is embedded within ```spigotpi``` and it inherits the ```use_lowlevel``` variable.  Although closures are not really needed for the Python implementation, I chose to write the code this way so that the function implementation is located next to where it is called from.

The closure functions were used to handle the normal Python operations or the Low level operations which mimick the assembly language based on the ```use_lowlevel``` variable.

An example of a low level operation is multiplying by 10 using left shifts such as:
```u = (N << 3) + (N << 1)```.

Note that above, I multiplied ```N``` by 10 before dividing by 3 so that I could avoid floating point math.

This low level closure pattern repeats itself through the Python code.

### Assertions

Asserting is a technique where a programmer can quickly see if the code is producing the right answer.  In the following ```for``` loop we check to make sure our result matches the well known Pi value that is available on the web.

```Python
    for i in range(0, check_len-1):
        assert(pi_str[i] == spigotpi_str[i+1])
```


If the strings did not match, the assert would generate an error to let us know the algorithm failed.  Using assertions is something I take advantage of in my daily programming as it helps to check current and future changes to the code.


