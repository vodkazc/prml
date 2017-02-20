import logging
from TraceParser import Trace
import matplotlib.pyplot as plt
if __name__ == '__main__':
    logging.basicConfig(filename='logger.log', level=logging.DEBUG)
    #sampleFile =
    plainFile = open('plain', 'wb')
    trace = Trace('D:\\trace\\aes\\aes_template.trs')
    trace.parseTraceHeader()
    #for i in range(0, trace.traceNumber-1):
    data = trace.getTrace(0)
    plainFile.write(data[1])

    plainFile.close()

    plainFile = open('plain', 'r')
    test = plainFile.read()


    #Fig = plt.figure(1)
    #axes = Fig.add_subplot(111)
    #axes.hold(False)
    #data = trace.getTrace(0)
    #axes.plot(data[2])
    #Fig.show()
    #Fig.hold()
