#
# mgpu.py - mainline test script for testing the virtual GPU
#

import mcs
import vgpu
import inspect

#
# Test functions
#   Compute shader classes declared as a closure
#

# Copy kernel to duplicate info from one buffer to another
def testCopyKernel():
    print("Test: %s" % vgpu.function_name())
   
    # Device
    device = vgpu.Device()
    print("\tDevice: %s" % device.name())
    
    # Buffer 8 by 8
    H = 8
    W = 8
    L = H * W
    buffer_in = device.newBufferWithSize(L)
    buffer_out = device.newBufferWithSize(L)

    # Initialize buffer_in
    for i in range(0,L):
        buffer_in.set(i,i+10)

    # Create kernel and pipeline state
    kernel = mcs.KernelCopy()
    kernel = vgpu.Kernel(kernel.run)
    pipeline_state = vgpu.PipelineState(kernel)

    # Dispatch thread setup
    threadsPerThreadGroup = vgpu.Size(1, 1, 1)
    threadsPerGrid = vgpu.Size(
        (H+threadsPerThreadGroup.x()-1)/threadsPerThreadGroup.x(),
        (W+threadsPerThreadGroup.y()-1)/threadsPerThreadGroup.y(),
        1)
   
    cmd_buf = device.commandBuffer()
    encoder = cmd_buf.computeCommandEncoder()
    encoder.setPipelinestate(pipeline_state)
    
    # Set the arguments
    encoder.addArg(buffer_in)
    encoder.addArg(buffer_out)
    encoder.addArg(H)
    encoder.addArg(W)

    encoder.dispatchThreads(threadsPerGrid, threadsPerThreadGroup) 
    cmd_buf.submit()

    assert( buffer_in.contents() == buffer_out.contents() )


# More complex workflow where we calculate x*x in one compute shader
# and then add value to itself in another shader
def test_x_times_x_plus_x_times_2():
    print("Test: %s" % vgpu.function_name())

    # Device
    device = vgpu.Device()
    print("\tDevice: %s" % device.name())
    
    # Buffer 8 by 8
    H = 8
    W = 8
    L = H * W
    buffer_in = device.newBufferWithSize(L)
    buffer_out = device.newBufferWithSize(L)
    buffer_result = device.newBufferWithSize(L)

    # Initialize buffer_in
    for i in range(0,L):
        buffer_in.set(i,i)

    # Create kernel and pipeline state
    kernelTimes = mcs.KernelXTimesX()
    kernelTimes2 = mcs.KernelXTimes2()
    kernel_times = vgpu.Kernel(kernelTimes.run)
    pipeline_state_times = vgpu.PipelineState(kernel_times)
    kernel_times2 = vgpu.Kernel(kernelTimes2.run)
    pipeline_state_times2 = vgpu.PipelineState(kernel_times2)

    # Dispatch thread setup
    threadsPerThreadGroup = vgpu.Size(1, 1, 1)
    threadsPerGrid = vgpu.Size(
        (H+threadsPerThreadGroup.x()-1)/threadsPerThreadGroup.x(),
        (W+threadsPerThreadGroup.y()-1)/threadsPerThreadGroup.y(),
        1)
   
    cmd_buf = device.commandBuffer()
    
    encoder_times = cmd_buf.computeCommandEncoder()
    encoder_times.setPipelinestate(pipeline_state_times)
    
    # Set the arguments
    encoder_times.addArg(buffer_in)
    encoder_times.addArg(buffer_out)
    encoder_times.addArg(H)
    encoder_times.addArg(W)

    encoder_times.dispatchThreads(threadsPerGrid, threadsPerThreadGroup)

    encoder_times2 = cmd_buf.computeCommandEncoder()
    encoder_times2.setPipelinestate(pipeline_state_times2)
    
    # Set the arguments
    encoder_times2.addArg(buffer_out)
    encoder_times2.addArg(buffer_result)
    encoder_times2.addArg(H)
    encoder_times2.addArg(W)

    encoder_times2.dispatchThreads(threadsPerGrid, threadsPerThreadGroup) 

    cmd_buf.submit()

    cpu_result = [i*i*2 for i in range(0,L)]
    assert( cpu_result == buffer_result.contents() )


#
# Main
#

def main():
    print("Executing tests:")

    # The simpliest of kernels - copy
    testCopyKernel()

    # Two kernels run together: result = x * x * 2
    test_x_times_x_plus_x_times_2()

if __name__ == "__main__":
    main()
