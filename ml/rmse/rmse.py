# RMSE Python script
# Simulates finding rmse error between cpu and gpu buffer results

import random
import math

random.seed(0)

Low = 1
High = 30

def rmse(N, factor, printArray):
    # Make an array for cpu data
    cpu_buffer = [random.randrange(Low,High) for i in range(0,N)]
    if printArray:
        print("CPU:\n", cpu_buffer)

    # Make an array for gpu data based on cpu plus some small delta
    # to simulate float point differences
    gpu_buffer = [(cpu_buffer[i]+random.random()*factor) for i in range(0,N)]
    if printArray:
        print("GPU:\n", gpu_buffer)

    sum = 0
    maxDiff = 0.0
    for i in range(0,N):
        diff = cpu_buffer[i] - gpu_buffer[i]
        squared_diff = diff ** 2
        sum += squared_diff
        abs_diff = math.fabs(diff) 
        if abs_diff > maxDiff:
            maxDiff = abs_diff
    rms_error = math.sqrt(sum / (float(N)))

    print("N:", N, "MaxDiff:", maxDiff, "Factor", factor, "RMSE:", rms_error)

def main():
    rmse(30000, 1e-5, False)
    rmse(30000, 0.01, False)
    rmse(30000, 0.1, False)
    rmse(30000, 1.0, False)


if __name__ == "__main__":
    main()

