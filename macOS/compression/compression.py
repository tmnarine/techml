#
# compression.py -- script to demonstrate how compression and decompression can be
# used to increase code performance. In this approach, you compress an application's large
# data files in the build system.  The application will load the now smaller file and
# decompress for usage.
#
# NOTE: it is possible that not all cases lead to increases in performance so exact scenarios must
# be tested carefully.
#

import tempfile
import lzma
import random
import time
import os


# Using a high resolution timer below so we convert from
# ns to ms
def ns_to_ms(duration_ns):
    return (1e-6 * duration_ns)


def build_large_array(size):
    # Repeat some numbers so that compression will make a difference
    return bytes([random.choice([0,0,0,33,55,87,99,99,1,2,3,1,1,1]) for i in range(0,size*4)])


def run(n):
    array = build_large_array(n*1024)
    array_compressed = lzma.compress(array)
 
    print("Array byte length %d Compressed byte length %d" % (len(array), len(array_compressed)))

    assert(len(array_compressed) <  len(array))
    
    # Write out the compressed and uncompressed files
    fc, fc_path = tempfile.mkstemp()
    with open(fc, 'wb') as file:
        file.write(array_compressed)

    f, f_path = tempfile.mkstemp()
    with open(f, 'wb') as file:
        file.write(array)

    # Load the uncompressed file as if we are in an application
    # and time the operation
    load_array_uncompressed = None
    start_time = time.perf_counter_ns()
    with open(f_path, 'rb') as file:
        load_array_uncompressed = file.read()
    end_time = time.perf_counter_ns()
    # print("\t%f %f" % (start_time, end_time))
    duration_f = end_time - start_time
    print("\tUncompressed load time %.2f ms" % (ns_to_ms(duration_f)))
    assert(load_array_uncompressed == array)

    # Load the compressed file as if we are in an application, apply
    # a decompress while timing both operations
    load_array_compressed = None
    start_time = time.perf_counter_ns()
    with open(fc_path, 'rb') as file:
        load_array_compressed = file.read()

    # Decompress the loaded array
    load_array_decompressed = lzma.decompress(load_array_compressed)
    end_time = time.perf_counter_ns()
    duration_fc = end_time - start_time
    # print("\t%f %f" % (start_time, end_time))
    print("\tLoad + Decompress total %.2f ms" % (ns_to_ms(duration_fc)))
    if duration_fc != 0.0:
        print("\tSpeed up %.2f (>1 is faster)" % (duration_f/duration_fc))
    else:
        print("\tFaster by %.2f ms" % (ns_to_ms(duration_f - duration_fc)))

    # Check that arrays are ok
    assert(len(load_array_compressed)>0)
    assert(len(load_array_decompressed)>0)
    assert(load_array_compressed != array)
    assert(load_array_decompressed == array)

    # Cleanup
    os.unlink(fc_path)
    os.unlink(f_path)


def main():
    for i in range(1,16):
        run(i)
    
if __name__ == '__main__':
    main()
