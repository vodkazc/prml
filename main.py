import logging
from TraceParser import Trace
from struct import pack
import io
import numpy
import matplotlib.pyplot as plt
if __name__ == '__main__':
    logging.basicConfig(filename='logger.log', level=logging.DEBUG)
    #sampleFile =
    #plainFile = open('plain', 'wb')
    trace = Trace('../aes_template.trs')
    trace.parsetraceheader()
    print('begin')
    data = trace.gettrace(0)
    a = numpy.array(data[2], numpy.float32)
    a = numpy.array()
    a.tofile('np', )
    print(a.dtype)
 #   fwrite = io.FileIO('../sampleData', 'wb+')
  #  for i in data[2]:


   #     fwrite.write(pack('<f', i))
   # fwrite = io.FileIO('../cryptoData', 'wb+')
    # for i in range(0, trace.traceNumber):
    #     data = trace.gettrace(i)
    #     fwrite.write(bytes(data[1]))
    #
    #fwrite.close()
    print('finish')
    #cryptoData = open('../cryptoData', 'wb')
    #cryptoData.write()
    #for i in range(0, trace.traceNumber-1):
    #data = trace.getTrace(0)
   # plainFile.write(data[1])

    #plainFile.close()

    #plainFile = open('plain', 'r')
    #test = plainFile.read()


    # Fig = plt.figure(1)
    # axes = Fig.add_subplot(111)
    # axes.hold(False)
    # data = trace.gettrace(0)
    # axes.plot(data[2])
    # Fig.show()
    # Fig.hold()
