
import numpy as np
from matplotlib.mlab import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

if __name__ == '__main__':
    # 60 dimention sample for aes first round first sbox out
    # sample is a 60000 * 60 matrix
    sample_raw = np.load('../s0_sample_60dim.npy')

    mypca = PCA(sample_raw)
    sample = mypca.project(sample_raw)
    # sample_raw_mean = np.mean(sample_raw, 0)
    # sample_raw_std = np.std(sample_raw, 0)
    # sample = (sample_raw - sample_raw_mean) / sample_raw_std
    # hwdata is first round sbox output 's hw, 60000*16 matrix
    hwdata = np.load('../soutHWMat.npy')

    # divide the sample into two group, one is 50000 samples for trainning
    # another one is 10000 samples for testing
    trainSample = sample[0:49999, :]
    testSample = sample[50000:59999, :]

    trainLabel = hwdata[0:49999, 0]
    testLabel = hwdata[50000:59999, :]

    # according to label , classify the train sample
    indexL = []
    for i in range(9):
        indexL.append(trainLabel == i)
    # result = (trainLabel == 0)
    sample_hw = []
    for i in range(9):
        sample_hw.append(trainSample[indexL[i], :])

    meanMat = []
    for i in range(9):
        meanMat.append(np.mean(sample_hw[i], 0))
        #plt.plot(meanMat[i], label=['hw' + str(i)])
    # sample_hw0 = trainSample[indexL[0], :]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(meanMat[0], meanMat[0])
    ax.scatter(meanMat[4], meanMat[4])
    ax.scatter(meanMat[8], meanMat[8])
    # plt.plot(sample_hw[0][:, 0] , sample_hw[0][:, 1])
    # plt.legend()
    plt.show()

    result = (hwdata[:, 0] == 0)
    print(hwdata[:, 0] == 0)

