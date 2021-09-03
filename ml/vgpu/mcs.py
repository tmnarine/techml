#
# mcs.py -- main compute shaders
#

import vgpu

# Decorator
def kernel(function):
    return vgpu.get_function_no_globals(function)

#
# Shaders (kernels)
#

class KernelCopy(vgpu.KernelObject):

    def __init__(self):
        super().__init__()

    @kernel
    def run(self, buffer_in, buffer_out, H, W, grid_pos, thread_pos):
        self._kernel_pre() # Start with this call
        
        in_idx = grid_pos.x() * W + grid_pos.y()
        out_idx = in_idx
        log_msg = ("\t\tkernelCopy: %d %d %s %s" % (H, W, grid_pos, thread_pos))
        buffer_out.set(out_idx, buffer_in.get(in_idx))

        return self._kernel_post(log_msg) # End with this return


class KernelXTimesX(vgpu.KernelObject):

    def __init__(self):
        super().__init__()

    @kernel
    def run(self, buffer_in, buffer_out, H, W, grid_pos, thread_pos):
        self._kernel_pre() # Start with this call
        
        in_idx = grid_pos.x() * W + grid_pos.y()
        out_idx = in_idx
        x = buffer_in.get(in_idx)
        buffer_out.set(out_idx, x*x)
        log_msg = ("\tkernel_x_times_x: %d %d %s %s %d" % (H, W, grid_pos, thread_pos, x*x))

        return self._kernel_post(log_msg) # End with this return


class KernelXTimes2(vgpu.KernelObject):

    def __init__(self):
        super().__init__()

    @kernel
    def run(self, buffer_in, buffer_out, H, W, grid_pos, thread_pos):
        self._kernel_pre() # Start with this call
        
        in_idx = grid_pos.x() * W + grid_pos.y()
        out_idx = in_idx
        x = buffer_in.get(in_idx)
        buffer_out.set(out_idx, x*2)
        log_msg = ("\tkernel_x_times_2: %d %d %s %s %d" % (H, W, grid_pos, thread_pos, x+x))

        return self._kernel_post(log_msg) # End with this return


class KernelNCHW_2_NHWC(vgpu.KernelObject):

    def __init__(self):
        super().__init__()

    @kernel
    def run(self, buffer_in, buffer_out, N, C, H, W, grid_pos, thread_pos):
        self._kernel_pre() # Start with this call

        n = int(grid_pos.x() / C)
        c = grid_pos.x() % C
        h = grid_pos.y()
        w = grid_pos.z()

        in_idx = n * C * H * W + c * H * W + h * W + w
        out_idx = n * H * W * C + h * W * C + w * C + c
        log_msg = ("\t\tKernelNCHW2NHWC: %d %d %d %d %s %s %d %d %d %d : %d %d" %
                    (N, C, H, W, grid_pos, thread_pos, n, c, h, w, in_idx, out_idx))
        buffer_out.set(out_idx, buffer_in.get(in_idx))

        return self._kernel_post(log_msg) # End with this return


class KernelNHWC_2_NCHW(vgpu.KernelObject):

    def __init__(self):
        super().__init__()

    @kernel
    def run(self, buffer_in, buffer_out, N, C, H, W, grid_pos, thread_pos):
        self._kernel_pre() # Start with this call
  
        n = int(grid_pos.x() / H)
        h = int(grid_pos.x() % H)
        w = grid_pos.y()
        c = grid_pos.z()
        in_idx = n * H * W * C + h * W * C + w * C + c
        out_idx = n * C * H * W + c * H * W + h * W + w

        log_msg = ("\t\tKernelNHWC2NCHW: %d %d %d %d %s %s %d %d %d %d : %d %d" %
                    (N, C, H, W, grid_pos, thread_pos, n, c, h, w, in_idx, out_idx))
        buffer_out.set(out_idx, buffer_in.get(in_idx))

        return self._kernel_post(log_msg) # End with this return
