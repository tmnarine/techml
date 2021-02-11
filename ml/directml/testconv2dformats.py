# Tensorfow testformats.py convolution script.
# Generic script tested with the DirectML version of Tensorflow with an AMD GPU
# NOTE: running in Idle does not show the GPU information.  Run on the command
# line to see lines such as the following:
#    ... tensorflow/core/common_runtime/dml/dml_device_cache.cc:109] DirectML:
#                       creating device on adapter 0 (AMD Radeon(TM) RX 5600M Series)

import numpy as np
import tensorflow as tf

#
# N - batch count
# H - data buffer height
# W - data buffer width
# I - input channels
# O - output channels
# R - Filter height
# S - Filter width
# keepDataConstant - initialize array to 1 if True else use incrementing numbers
# keepWeightConstant - initialize to 1 if Ttue else use incrementing numbers
# df - data format
# deviceid = GPU device ID string
#
def TensorFlowTest(N, H, W, R, S, I, O, keepDataConstant, keepWeightConstant, deviceid, df="NHWC"):
    assert(R==S)
    assert(df=="NCHW" or df=="NHWC")

    C = I

    if df=="NHWC":
        print("TensorFlowTest: ", df, N, H, W, C, " RSIO: ", R, S, I, O, keepDataConstant, keepWeightConstant)
    else:
        print("TensorFlowTest: ", df, N, C, H, W, " RSIO: ", R, S, I, O, keepDataConstant, keepWeightConstant)

    # GPU setup
    gpu_config = tf.compat.v1.GPUOptions()
    gpu_config.visible_device_list = deviceid

    # Create the data buffer using np
    length=N*C*H*W
    np_linear_data=np.array([(1.0 if keepDataConstant else i+1) for i in range(length)])
    if df=="NHWC":
        np_data = np_linear_data.reshape(N, H, W, C)
    else:
        np_data = np_linear_data.reshape(N, C, H, W)
    print("Data Shape: ",str(np_data.shape))
    print("Data: ")
    print(np_data)

    # Create the weights buffer using np
    length=R*S*I*O
    np_linear_weights = np.array([(1.0 if keepWeightConstant else i+1) for i in range(length)])
    np_weights = np_linear_weights.reshape(R, S, I, O)
    print("Weight Shape: ",str(np_weights.shape))
    print("Weights: ")
    print(np_weights)

    # Convert np arrays to tensors
    tensor_data = tf.constant(np_data, dtype=tf.float32)
    tensor_weights = tf.constant(np_weights, dtype=tf.float32)

    # Create a session to run the conv2d as directml support is in an older version of Tensorflow
    session=tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(gpu_options=gpu_config))

    tensor_result = session.run(
            tf.nn.conv2d( tensor_data, tensor_weights, strides=(1,1,1,1), padding='VALID', data_format=df)
        )

    print("Result Shape: ", str(tensor_result.shape))
    print("Result: ")
    print(tensor_result)

    return tensor_result


def main():
    result_nchw = TensorFlowTest(1, 12,12, 3, 3, 4, 4, False, False, "0", "NCHW" )
    result_nhwc = TensorFlowTest(1, 12,12, 3, 3, 4, 4, False, False, "0", "NHWC" )

    assert( result_nchw.shape != result_nhwc.shape )


if __name__ == "__main__":
    main()


