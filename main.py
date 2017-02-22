import logging
from TraceParser import Trace
from struct import pack
import io
import numpy as np
import myutil
import aes128
import matplotlib.pyplot as plt
if __name__ == '__main__':
    logging.basicConfig(filename='logger.log', level=logging.ERROR)
    cryptoDataMatFileName = '../cryptoDataMat.npy'
    sampleFileName = '../sampleMat.npy'
    soutValueFileName = '../soutValueMat.npy'
    cryptoDataMat = np.load(soutValueFileName)
    # hammingMat = np.zeros((1, 256), 'B')
    # mm = myutil.MyUtil()
    # for i in range(256):
    #     hammingMat[0, i] = mm.calHW(i)
    # np.save('../hwMat', hammingMat)
    # hwMat = np.load('../hwMat.npy')
    # cryptoDataHW = hwMat[0, cryptoDataMat]
    # np.save('../soutHWMat.npy', cryptoDataHW)
    # print('h')
    # print(cryptoDataMat.shape[0])
    # key = [43, 126, 21, 22, 40, 174, 210, 166, 171, 247, 21, 136, 9, 207, 79, 60]
    # sampleMat = numpy.load(sampleFileName, 'r')
    # aes = aes128.AES128(key)
    # soutMat = aes.getsout(cryptoDataMat)
    # np.save('../soutValueMat', soutMat)
    # print(soutMat)
    # cryptoData = (numpy.fromfile(cryptoDataFileName, 'B'))
    # print(cryptoData[59998])
    # print('hello')
    # trace = Trace('D:\\trace\\aes\\aes_template.trs')
    # trace.parsetraceheader()
    # trace.extractcryptodata(cryptoDataFileName, sampleFileName)
    # cryptoDataArray = numpy.fromfile(cryptoDataFileName, 'uint8')
    # cryptoDataMat = cryptoDataArray.reshape(60000, 32)
    # numpy.save('../cryptoDataMat', cryptoDataMat)
    # mat = numpy.load('../cryptoDataMat.npy')
    # print('hello')
    # sampleMat = numpy.fromfile(sampleFileName, 'float32').reshape(60000, 16321)
    # numpy.save('../sampleMat', sampleMat)
    # data = numpy.fromfile(sampleFileName, 'float32')
    # data1 = data.reshape((100, 16321))
    # print("hello")
    # data = trace.gettrace(59999)
    # print(data[1])
    # data = trace.gettrace(1)
    # print(data[1])
    # fcrypto = io.FileIO(cryptoDataFileName, 'wb+')
    # # fsamle = io.FileIO(samplename, 'wb+')
    # for i in range(0, self.traceNumber):
    #     data = self.gettrace(i)
    #     fcrypto.write(bytes(data[1]))
    #     for j in data[2]:
    #         fsamle.write(pack('<f', j))
    #     if i % 100 == 0:
    #         print(i)
    # fcrypto.close()
    # fsamle.close()
    # Fig = plt.figure(1)
    # axes = Fig.add_subplot(111)
    # axes.hold(False)
    # data = trace.gettrace(0)
    # axes.plot(data[2])
    # Fig.show()
    # Fig.hold()
