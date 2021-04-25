#
# Main script for testing the virtual GPU
#

import vgpu
import inspect


def testCopyKernel():
    print("Test: %s" % _fn_name())

    class KernelGrayscale(vgpu.KernelObject):

        def __init__(self):
            super().__init__()

        # GPU kernel 
        def run(self, buffer_in, buffer_out, H, W, grid_pos, thread_pos):
            self._kernel_pre() # Start with this call
            
            in_idx = grid_pos.x() * W + grid_pos.y()
            out_idx = in_idx
            log_msg = ("\t\tkernelGrayscale: %d %d %s %s" % (H, W, grid_pos, thread_pos))
            buffer_out.set(out_idx, buffer_in.get(in_idx))

            return self._kernel_post(log_msg) # End with this return
   
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
    kernel = KernelGrayscale()
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


def test_x_times_x_plus_x():
    print("Test: %s" % _fn_name())

    class KernelXTimesX(vgpu.KernelObject):

        def __init__(self):
            super().__init__()

        # GPU kernel 
        def run(self, buffer_in, buffer_out, H, W, grid_pos, thread_pos):
            self._kernel_pre() # Start with this call
            
            in_idx = grid_pos.x() * W + grid_pos.y()
            out_idx = in_idx
            x = buffer_in.get(in_idx)
            buffer_out.set(out_idx, x*x)
            log_msg = ("\tkernel_x_times_x: %d %d %s %s %d" % (H, W, grid_pos, thread_pos, x*x))

            return self._kernel_post(log_msg) # End with this return

    class KernelXPlusX(vgpu.KernelObject):

        def __init__(self):
            super().__init__()
            
        def run(self, buffer_in, buffer_out, H, W, grid_pos, thread_pos):
            self._kernel_pre() # Start with this call
            
            in_idx = grid_pos.x() * W + grid_pos.y()
            out_idx = in_idx
            x = buffer_in.get(in_idx)
            buffer_out.set(out_idx, x+x)
            log_msg = ("\tkernel_x_plus_x: %d %d %s %s %d" % (H, W, grid_pos, thread_pos, x+x))

            return self._kernel_post(log_msg) # End with this return

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
    kernelTimes = KernelXTimesX()
    kernelPlus = KernelXPlusX()
    kernel_times = vgpu.Kernel(kernelTimes.run)
    pipeline_state_times = vgpu.PipelineState(kernel_times)
    kernel_plus = vgpu.Kernel(kernelPlus.run)
    pipeline_state_plus = vgpu.PipelineState(kernel_plus)

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

    encoder_plus = cmd_buf.computeCommandEncoder()
    encoder_plus.setPipelinestate(pipeline_state_plus)
    
    # Set the arguments
    encoder_plus.addArg(buffer_out)
    encoder_plus.addArg(buffer_result)
    encoder_plus.addArg(H)
    encoder_plus.addArg(W)

    encoder_plus.dispatchThreads(threadsPerGrid, threadsPerThreadGroup) 

    cmd_buf.submit()

    cpu_result = [i*i+i*i for i in range(0,L)]
    assert( cpu_result == buffer_result.contents() )


#
# Local utility functions
#

def _fn_name():
    return inspect.stack()[1][3]


#
# Main
#

def main():
    print("Executing tests:")

    # The simpliest of kernels - copy
    testCopyKernel()

    # Two kernels run together: result = x * x + x
    test_x_times_x_plus_x()

if __name__ == "__main__":
    main()
