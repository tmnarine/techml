# techml
Technical notes and machine language scripts written in various programming languages.

## Technical Notes

### Objective-C selectors and the 2 argument invokation limit
Selectors in Objective-C support a very dynamic programming model.  This programming construct make it possible to check at runtime if specific methods are implemented.  Method lookup is very useful for handling code compatiblity between components that may be loosely connected.  Selectors invokation though, come with a restriction of only allowing two parameters.  See the following [technote](macOS/objcselectors/README.md) on how to work around this limitation.

## Machine Learning

### Running Tensorflow DirectML on AMD Hardware
A small [example](ml/directml/testconv2dformats.py) that demonstrates how to run the [DirectML version of TensorFlow](https://docs.microsoft.com/en-us/windows/win32/direct3d12/gpu-tensorflow-wsl) on AMD GPUs.  Use the DirectML link to learn how setup your Python and Tensorflow modules.  Code is for generic simple convolution and is a good starting point for working with an AMD GPU. 

### Root Mean Square Error (RMSE)
In datascience, RMSE is used to find the error between predicted and observed values.  Given n predicted and observed values, you find the result of the following:

![Equation](doc/image/rmse.png)

This error calculation is also useful in areas such as machine learning.  Comparing the RMSE of an algorithm run on the CPU versus GPU can be used to get a handle on accurracy.
Here is a simple [example](ml/rmse/rmse.py) that demonstrates the use of RMSE.

### Virtual GPU in Python
It is an understatement to say that working with machine learning algorithms is complex.  I have found it useful to prototype various bits of functionality in Python.  This example code takes prototyping a step further and allows the mimicking of a virtual GPU in Python.  Required objects such as Devices, Buffers, Encoders, Command Buffers can be implemented for simple GPGPU workflows.  The intention is to move some of the required thinking/prototyping further left in the development cycle(assuming that you work in a left to right domain). There are two Python files:
*[mgpu - main samples ](ml/vgpu/mgpu.py)
*[vgpu - a virtual GPU](ml/vgpu/vgpu.py)

