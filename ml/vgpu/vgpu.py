#
# Python script that emulates a simple virtual GPU:
# - Script written in Metal style rather than Vk or DX
# - Virtual GPU loosely based on AMD
# - Handles floats only for simple memory model
# - GPGPU
#
# Based on information from:
#   https://gpuopen.com/learn/optimizing-gpu-occupancy-resource-usage-large-thread-groups/
#   https://rastergrid.com/blog/gpu-tech/2021/01/understanding-gpu-caches/
#   https://gpuopen.com/performance/
#   https://www.amd.com/system/files/documents/rdna-whitepaper.pdf
#   
#
# 1.  A GPU has a number of CUs(compute units or cores) such as 40, 56, 64
# 2.  Each CU contains 4 SIMDs
# 3.  Smallest unit of scheduled work to run on a CU is a wave
# 4.  Each wave contains 64 threads
# 5.  Each SIMD in a CU can schedule 10 waves in parallel.
# 6.  Each CU can have 40 waves in progress, 64 threads each,
#     totalling up to 2560 threads / CU
# 7.  GPU instruction set caches are immportant because a cache
#     miss can stall many threads.  But this type of cache won't
#     be considered in vgpu
# 8.  Data caches per CU will be considered
# 9.  Data caches per CU/core is more like a coalescing buffer for
#     memory operations (read operations)
# 10. Writes propagate to the next level cache.
#
# Outstanding work:
# 1. Add a Python generator for simulating threads
# 2. Calculate occupancy
# 3. Add simple memory model and evaluate data cache line misses using
#    spatial and temporal properties of the threads
# 4. More variation and testing
#

import inspect
import types
import builtins

# Globals
DeviceCounter = 0

# Config - not really used now
class _VGPU:
    CUs                 = 40
    SIMDs               = 4
    SIMD_PARALLEL_WAVES = 10
    THREADS_PER_WAVE    = 64
    CACHE_LINE_SIZE     = 4

#
# Classes
#

# self._logmsg controls if log output is on or off
class Device:

    def __init__(self):
        global DeviceCounter
        self._id = DeviceCounter
        DeviceCounter += 1
        self._config = _VGPU()
        self._logmsg = False
        # Build the read/write caches
        self._cacheLineManager = _CacheLineManager(self._config)

    def name(self):
        return ("vgpu%d" % (self._id))

    def commandBuffer(self):
        return CommandBuffer(self)
        
    def newBufferWithSize(self, size):
        return Buffer(self, size)

    def run(self, function, function_args, threadsPerGrid, threadsPerThreadGroup):
        if len(function_args) == 0:
            print("\tWarning: no kernel arguments set")
        print("\tRunning kernel")
        print("\t\t", end="")
        #
        counter = 0
        for i in range(0, threadsPerGrid.x()):
            for j in range(0, threadsPerGrid.y()):
                for k in range(0, threadsPerGrid.z()):
                    for l in range(0, threadsPerThreadGroup.x()):
                        for m in range(0, threadsPerThreadGroup.y()):
                            for n in range(0, threadsPerThreadGroup.z()):
                                grid_pos = Size(i, j, k)
                                thread_pos = Size(l, m, n)
                                thread_args = function_args + [grid_pos, thread_pos]
                                # Invoke the function
                                if counter == 0:
                                    (kernel_msg, log_msg) = function(*thread_args)
                                else:
                                    (nop_msg, log_msg) = function(*thread_args)
                                    print(".", end="")
                                if self._logmsg:
                                    print(log_msg)
                                counter += 1

        #
        print("\n\tDone")
        print("\tSummary:")
        print("\t\t%s" % kernel_msg)
        print("\t\tBuffer statistics:")
        for arg in (function_args):
            if isinstance(arg, Buffer):
                arg.setOnGPU(False)
                (reads, writes) = arg.stats()
                print("\t\t\tRead: %.2f%% Write %3.2f%%" % (100*reads/arg.size(), 100*writes/arg.size()))
        

class CommandBuffer:

    def __init__(self, device):
        self.__commands = []
        self.__device = device

    def computeCommandEncoder(self):
        encoder = ComputeEncoder(self.__device)
        self.__commands.append(encoder)
        return encoder

    def submit(self):
        for cmd in self.__commands:
            cmd.run()


class Buffer:

    def __init__(self, device, size):
        self.__buffer = [0 for i in range(size)]
        self.__reads = 0
        self.__writes = 0
        self.__ongpu = False
        self.__device = device

    def setOnGPU(self, state):
        self.__ongpu = state

    def contents(self):
        return [] if self.__ongpu else self.__buffer

    def get(self, index):
        # Only track changes once encoded to GPU
        if self.__ongpu:
            self.__reads += 1
        return self.__buffer[index]

    def set(self, index, value):
        # Only track changes once encoded to GPU
        if self.__ongpu:
            self.__writes += 1
        self.__buffer[index] = value

    def size(self):
        return len(self.__buffer)

    def stats(self):
        return (self.__reads, self.__writes)


class Size:

    def __init__(self, x, y, z):
        self.__x = int(x)
        self.__y = int(y)
        self.__z = int(z)

    def x(self):
        return self.__x

    def y(self):
        return self.__y

    def z(self):
        return self.__z

    def __str__(self):
        return ("(%d, %d, %d)" % (self.x(), self.y(), self.z()))


class KernelObject:
    
    def __init__(self):
        self.__line = 0

    def _fn_fn_name(self):
        return inspect.currentframe().f_back.f_back.f_code.co_name

    def _fn_fn_line_no(self):
        return inspect.currentframe().f_back.f_back.f_lineno

    def _kernel_pre(self):
        self.__line = self._fn_fn_line_no()

    def _kernel_post(self,log_msg):
        kernel_length = self._fn_fn_line_no() - self.__line + 1
        msg = ("Warning - long kernel function: %d lines" % kernel_length) if kernel_length > 30 else ("%d lines" % kernel_length)
        return ("Kernel: %s : %s" % ((self._fn_fn_name(), msg)), log_msg)

    # Override this
    def run(self):
        assert( False )


class Function:

    def __init__(self, name):
        self.__name = name
        
        
class Kernel:

    def __init__(self, function):
        assert( callable(function) )
        self.__function = function

    def function(self):
        return self.__function


class PipelineState:

    def __init__(self, kernel):
        self.__kernel = kernel

    def kernel(self):
        return self.__kernel

        
class ComputeEncoder:

    def __init__(self, device):
        self.__pipelinestate = None
        self.__threadsPerGrid = None
        self.__threadsPerThreadGroup = None
        self.__device = device
        self.__args = []

    def addArg(self, arg):
        self.__args.append(arg)
        #
        if isinstance(arg, Buffer):
                arg.setOnGPU(True)

    def setPipelinestate(self, pipelinestate):
        self.__pipelinestate = pipelinestate

    def dispatchThreads(self, threadsPerGrid, threadsPerThreadGroup):
        if self.__pipelinestate:
            self.__threadsPerGrid = threadsPerGrid
            self.__threadsPerThreadGroup = threadsPerThreadGroup
            print("\tthreadsPerThreadGroup(%d, %d, %d)" %
                  (threadsPerThreadGroup.x(), threadsPerThreadGroup.y(), threadsPerThreadGroup.z()))
            print("\tthreadsPerGrid(%d, %d, %d)" %
                  (threadsPerGrid.x(), threadsPerGrid.y(), threadsPerGrid.z()))
        else:
            print("\tWarning: No pipelinestate set")

    def run(self):
        if len(self.__args) == 0:
            print("\tWarning: no kernel arguments set")
        # Get the function
        function = self.__pipelinestate.kernel().function()
        #
        self.__device.run(function, self.__args, self.__threadsPerGrid, self.__threadsPerThreadGroup)


# Unused - tbd
class _CacheLineManager:

    def __init__(self, config):
        self.__line = [-1, -1, -1, -1]
        self.__loads = 0
        self.__stores = 0
        self.__miss = 0
        self.__config = config
        assert(len(self.__line) == self.__config.CACHE_LINE_SIZE)

    def load(self, index):
        if self.__line[0] == index:
            return
        for l in range(0,len(self.__line)):
            self.__line[l] = index + l
        self.__loads += 1
        # Don't allow mixing of load/store
        assert(self.__stores == 0)

    def store(self, index):
        if self.__line[0] == index:
            return
        for l in range(0,len(self.__line)):
            self.__line[l] = index + l
        self.__stores += 1
        # Don't allow mixing of load/store
        assert(self.__loads == 0)

    def cache(self, index):
        incache = index in self.__line
        if not incache:
           self.__miss += 1
           load( index )

    def stats(self):
        return (self.__loads, self.__stores, self.__miss) 

   
# Utility to remove globals from a function.  This will be called using a decorator
# against the GPU execute method
def get_function_no_globals(function):
    assert(function)
    builtin_globals = {'__builtins__': builtins}
    code = function.__code__
    function_defaults = function.__defaults__
    # Build the new function - see help(types.FunctionType)
    new_function = types.FunctionType(code, globals=builtin_globals, argdefs=function_defaults)
    new_function.__annotations__ = function.__annotations__
    return new_function
    
