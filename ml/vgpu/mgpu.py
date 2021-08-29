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


def test_nchw_nhwc_conversion(N, C, H, W):
    print("Test: %s" % vgpu.function_name())

    # Device
    device = vgpu.Device()
    print("\tDevice: %s" % device.name())
    
    # Buffer
    L = N * C * H * W
    assert(L > 0)
    buffer_nchw_in = device.newBufferWithSize(L)
    buffer_nhwc_out = device.newBufferWithSize(L)
    buffer_nchw_out = device.newBufferWithSize(L)

    # Initialize buffer_in
    for i in range(0,L):
        buffer_nchw_in.set(i,i)

    # Create kernel and pipeline state
    kernelNCHW_2_NHWC = mcs.KernelNCHW_2_NHWC()
    kernelNHWC_2_NCHW = mcs.KernelNHWC_2_NCHW()
    kernel_NCHW_2_NHWC = vgpu.Kernel(kernelNCHW_2_NHWC.run)
    pipeline_state_NCHW_2_NHWC = vgpu.PipelineState(kernel_NCHW_2_NHWC)
    kernel_NHWC_2_NCHW = vgpu.Kernel(kernelNHWC_2_NCHW.run)
    pipeline_state_NHWC_2_NCHW = vgpu.PipelineState(kernel_NHWC_2_NCHW)

    # Dispatch thread setup
    threadsPerThreadGroup = vgpu.Size(1, 1, 1)
    threadsPerGrid = vgpu.Size(
        N * C,
        (H+threadsPerThreadGroup.x()-1)/threadsPerThreadGroup.x(),
        (W+threadsPerThreadGroup.y()-1)/threadsPerThreadGroup.y() )
   
    cmd_buf = device.commandBuffer()
    
    encoder_nchw_nhwc = cmd_buf.computeCommandEncoder()
    encoder_nchw_nhwc.setPipelinestate(pipeline_state_NCHW_2_NHWC)
    
    # Set the arguments
    encoder_nchw_nhwc.addArg(buffer_nchw_in)
    encoder_nchw_nhwc.addArg(buffer_nhwc_out)
    encoder_nchw_nhwc.addArg(N)
    encoder_nchw_nhwc.addArg(C)
    encoder_nchw_nhwc.addArg(H)
    encoder_nchw_nhwc.addArg(W)

    encoder_nchw_nhwc.dispatchThreads(threadsPerGrid, threadsPerThreadGroup)

    encoder_nhwc_nchw = cmd_buf.computeCommandEncoder()
    encoder_nhwc_nchw.setPipelinestate(pipeline_state_NHWC_2_NCHW)

    # Dispatch thread setup
    threadsPerThreadGroup = vgpu.Size(1, 1, 1)
    threadsPerGrid = vgpu.Size(
        N * H,
        (W+threadsPerThreadGroup.x()-1)/threadsPerThreadGroup.x(),
        (C+threadsPerThreadGroup.y()-1)/threadsPerThreadGroup.y() )

    # Set the arguments
    encoder_nhwc_nchw.addArg(buffer_nhwc_out)
    encoder_nhwc_nchw.addArg(buffer_nchw_out)
    encoder_nhwc_nchw.addArg(N)
    encoder_nhwc_nchw.addArg(C)
    encoder_nhwc_nchw.addArg(H)
    encoder_nhwc_nchw.addArg(W)

    encoder_nhwc_nchw.dispatchThreads(threadsPerGrid, threadsPerThreadGroup) 

    cmd_buf.submit()

    if L > 1:
        assert( buffer_nchw_in.notEquals(buffer_nhwc_out) )
        assert( buffer_nhwc_out.notEquals(buffer_nchw_out) )
    assert( buffer_nchw_in.equals(buffer_nchw_out) )


#
# Main
#

def main():
    print("Executing tests:")

    # The simpliest of kernels - copy
    testCopyKernel()

    # Two kernels run together: result = x * x * 2
    test_x_times_x_plus_x_times_2()

    # Run two kernels to perform data format conversion
    # and verify the result
    test_nchw_nhwc_conversion(1, 1, 1, 1)
    test_nchw_nhwc_conversion(1, 3, 5, 6)
    test_nchw_nhwc_conversion(1, 3, 6, 5)
    test_nchw_nhwc_conversion(4, 6, 12, 12)

if __name__ == "__main__":
    main()
