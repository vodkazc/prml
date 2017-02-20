# TraceParser.py --- parsing the .trs file
# Author: Zhang Chi
# Email:vodkazc@gmail.com
# Date: 2016.06.08

import logging
from struct import pack, unpack
from ctypes import *


# load C library
try:
    libc = cdll.msvcrt       # Windows
except AttributeError:
    libc = CDLL("libc.so.6")  # Linux


class CommonFile(object):
    """Common File Object for IO"""

    def __init__(self, path):
        self.path = path
        self.byteNum = 0
        self.fileHandler = None
        self.fileHandlerC = None

    def openfile(self, mode):
        # if os.path.exists(self.path):
        if mode[0] == 'r':
            # in read mode
            self.fileHandler = open(self.path, mode)
        else:
            # in write/append mode
            libc.fopen.restype = c_void_p
            libc.fopen.argtypes = c_char_p, c_char_p
            self.fileHandlerC = libc.fopen(self.path.encode('utf-8'), mode.encode('utf-8'))
        # return True
        # else:
        #     logging.info(self.path + 'does not exist.')
        #     return False

    def closeFile(self):
        if self.fileHandler:
            self.fileHandler.close()
            self.byteNum = 0
        return True

    def closeFileC(self):
        if self.fileHandlerC:
            libc.fclose.argtypes = c_void_p,
            libc.fclose.restype  = c_int
            libc.fclose(self.fileHandlerC)
            self.byteNum = 0
        return True

    def writeFile(self, point_list):
        libc.fwrite.argtypes = c_void_p ,c_size_t, c_size_t, c_void_p
        libc.fwrite.restype  = c_size_t
        # generate a c-style string buffer from python list
        c_buf = (c_float*len(point_list))(*point_list)
        n_items = libc.fwrite(c_buf, 4, len(point_list), self.fileHandlerC)
        # print('points written: ',n_items, ', actual points: ',len(point_list))
        return True

    def writeByte(self, byte_str):
        libc.fwrite.argtypes = c_void_p ,c_size_t, c_size_t, c_void_p
        libc.fwrite.restype  = c_size_t
        # print(byte_str)
        n_items = libc.fwrite(byte_str, 1, len(byte_str), self.fileHandlerC)
        return True


    def readByte(self, num):
        byte_re = self.fileHandler.read(num)
        self.byteNum += num
        return byte_re

    def readInt(self, num=4):
        byte_re = self.fileHandler.read(num)
        self.byteNum += num
        return int.from_bytes(byte_re, 'little')

    def readFloat(self, num=4):
        byte_re = self.fileHandler.read(num)
        self.byteNum += num
        return float.fromhex(byte_re.hex())

    def readStr(self, num):
        byte_re = self.fileHandler.read(num)
        self.byteNum += num
        return byte_re.decode()


    def seekFile(self, num=0):
        self.fileHandler.seek(num, 0)
        return True


class Trace(object):
    """Trace Class for .trs file"""

    def __init__(self, path):
        self.path = path
        self.traceFile = CommonFile(self.path)
        self.TraceSetObjects = {b'\x41': 'NT', b'\x42': 'NS', b'\x43': 'SC', b'\x44': 'DS', b'\x45': 'TS',
                                b'\x46': 'GT', b'\x47': 'DC', b'\x48': 'XO', b'\x49': 'XL', b'\x4A': 'YL',
                                b'\x4B': 'XS', b'\x4C': 'YS', b'\x4D': 'TO', b'\x4E': 'LS', b'\x5F': 'TB'}
        self.TraceHeader = {}
        self.headerLength = 0
        self.traceNumber = -1
        self.pointCount = -1
        self.sampleCoding = -1
        self.sampleLength = 0
        self.cryptoDataLength = 0
        self.titleSpace = 0
        self.globalTraceTitle = 'trace'
        self.description = None
        self.xAxisOffset = 0
        self.xLabel = ''
        self.yLabel = ''
        self.xAxisScale = 0
        self.yAxisScale = 0
        self.traceOffsetForDisp = 0
        self.logScale = 0
        # self.parseTraceHeader()

    def readHeaderDataLength(self):
        data_length = self.traceFile.readInt(1)
        if data_length & 0x80:
            data_length &= 0x7F
            data_length = self.traceFile.readInt(data_length)
        return data_length

    def parseTraceHeader(self):
        logging.info('Parsing Trace Header')
        self.traceFile.openfile('rb')
        while True:
            ch = self.traceFile.readByte(1)

            if ch not in self.TraceSetObjects:
                logging.error('Unknown Trace Header :' + ch.hex())
                raise ValueError('Unknown Trace Header :' + ch.hex())
            if ch == b'\x5F':
                logging.debug('Parsing Trace File End.')
                self.readHeaderDataLength()
                self.headerLength = self.traceFile.byteNum
                logging.debug('Trace Header Length : ' + str(self.headerLength))
                break
            if ch == b'\x41':
                logging.debug('Parsing Trace Header ' + ch.hex())
                data_length = self.readHeaderDataLength()
                if data_length != 4:
                    logging.error('Wrong trace header : ' + ch.hex())
                    raise ValueError('Wrong Trace Header')
                self.traceNumber = self.traceFile.readInt(data_length)
                logging.debug('Trace Number : ' + str(self.traceNumber))
            if ch == b'\x42':
                logging.debug('Parsing Trace Header ' + ch.hex())
                data_length = self.readHeaderDataLength()
                if data_length != 4:
                    logging.error('Wrong trace header : ' + ch.hex())
                    raise ValueError('Wrong Trace Header')
                self.pointCount = self.traceFile.readInt(data_length)
                logging.debug('Point Count : ' + str(self.pointCount))
            if ch == b'\x43':
                logging.debug('Parsing Trace Header ' + ch.hex())
                data_length = self.readHeaderDataLength()
                if data_length != 1:
                    logging.error('Wrong Trace Header : ' + ch.hex())
                    raise ValueError('Wrong Trace Header')
                value_tmp = self.traceFile.readInt(1)
                self.sampleCoding = (value_tmp & 0x10)
                self.sampleLength = value_tmp & 0x0F
                logging.debug('Sample Coding : ' + str(self.sampleCoding))
                logging.debug('Sample Length : ' + str(self.sampleLength))
            if ch == b'\x44':
                logging.debug('Parsing Trace Header ' + ch.hex())
                data_length = self.readHeaderDataLength()
                if data_length != 2:
                    logging.error('Wrong Trace Header : ' + ch.hex())
                    raise ValueError('Wrong Trace Header')
                self.cryptoDataLength = self.traceFile.readInt(data_length)
                logging.debug('Crypto Data Length : ' + str(self.cryptoDataLength))
            if ch == b'\x45':
                logging.debug('Parsing Trace Header ' + ch.hex())
                data_length = self.readHeaderDataLength()
                if data_length != 1:
                    logging.error('Wrong Trace Header : ' + ch.hex())
                    raise ValueError('Wrong Trace Header')
                self.titleSpace = self.traceFile.readInt(data_length)
                logging.debug('Title Space : ' + ch.hex())
            if ch == b'\x46':
                logging.debug('Parsing Trace Header ' + ch.hex())
                data_length = self.readHeaderDataLength()
                self.globalTraceTitle = self.traceFile.readStr(data_length)
                logging.debug('Global Trace Title : ' + self.globalTraceTitle)
            if ch == b'\x47':
                logging.debug('Parsing Trace Header ' + ch.hex())
                data_length = self.readHeaderDataLength()
                self.description = self.traceFile.readStr(data_length)
                logging.debug('Description : ' + self.description)
            if ch == b'\x48':
                logging.debug('Parsing Trace Header ' + ch.hex())
                data_length = self.readHeaderDataLength()
                if data_length != 4:
                    logging.error('Wrong Trace Header : ' + ch.hex())
                    raise ValueError('Wrong Trace Header : ' + ch.hex())
                self.xAxisOffset = self.traceFile.readInt()
                logging.debug('X-axis Offset : ' + str(self.xAxisOffset))
            if ch == b'\x49':
                logging.debug('Parsing Trace Header ' + ch.hex())
                data_length = self.readHeaderDataLength()
                self.xLabel = self.traceFile.readStr(data_length)
                logging.debug('X Label : ' + self.xLabel)
            if ch == b'\x4A':
                logging.debug('Parsing Trace Header ' + ch.hex())
                data_length = self.readHeaderDataLength()
                self.yLabel = self.traceFile.readStr(data_length)
                logging.debug('Y Label : ' + self.yLabel)
            if ch == b'\x4B':
                logging.debug('Parsing Trace Header ' + ch.hex())
                data_length = self.readHeaderDataLength()
                if data_length != 4:
                    logging.error('Wrong Trace Header : ' + ch.hex())
                    raise ValueError
                self.xAxisScale = self.traceFile.readFloat(data_length)
                logging.debug('X-axis Scale : ' + str(self.xAxisScale))
            if ch == b'\x4C':
                logging.debug('Parsing Trace Header ' + ch.hex())
                data_length = self.readHeaderDataLength()
                if data_length != 4:
                    logging.error('Wrong Trace Header : ' + ch.hex())
                    raise ValueError
                self.yAxisScale = self.traceFile.readFloat(data_length)
                logging.debug('Y-axis Scale : ' + str(self.xAxisScale))
            if ch == b'\x4D':
                logging.debug('Parsing Trace Header ' + ch.hex())
                data_length = self.readHeaderDataLength()
                if data_length != 4:
                    logging.error('Wrong Trace Header : ' + ch.hex())
                    raise ValueError
                self.traceOffsetForDisp = self.traceFile.readInt(data_length)
                logging.debug('Trace Offet For Displying : ' + self.traceOffsetForDisp)
            if ch == b'\x4E':
                logging.debug('Parsing Trace Header ' + ch.hex())
                data_length = self.readHeaderDataLength()
                if data_length != 1:
                    logging.error('Wrong Trace header : ' + ch.hex())
                    raise ValueError
                self.logScale = self.traceFile.readInt(1)
                logging.debug('Log Scale : ' + str(self.logScale))

        self.traceFile.closeFile()
        return True

    def getTrace(self, index):
        if index < 0 or index > self.traceNumber - 1:
            logging.error('Wrong Trace Index')
            raise ValueError('Wrong Trace Index')

        samplePoint = ()
        traceTitle = ''
        cryptoData = None
        self.traceFile.openfile('rb')
        self.traceFile.seekFile(self.headerLength + index * (self.titleSpace + self.cryptoDataLength + self.pointCount))
        if self.titleSpace != 0:
            traceTitle = self.traceFile.readStr(self.titleSpace).decode('utf-8')
            logging.debug('Trace %d title : %s' % (index, traceTitle))
        if self.cryptoDataLength != 0:
            cryptoData = list(self.traceFile.readByte(self.cryptoDataLength))
            logging.debug('CryptoData:' + str(cryptoData))
        if self.pointCount != 0:
            if self.sampleCoding == 0:
                bstr = self.traceFile.readByte(self.sampleLength * self.pointCount)
                if self.sampleLength == 1:
                    samplePoint = unpack(str(self.pointCount) + 'B', bstr)
                elif self.sampleLength == 2:
                    samplePoint = unpack('<' + str(self.pointCount) + 'H', bstr)
                elif self.sampleLength == 4:
                    samplePoint = unpack('<' + str(self.pointCount) + 'I', bstr)
            else:
                bstr = self.traceFile.readByte(self.sampleLength * self.pointCount)
                samplePoint = unpack('<' + str(self.pointCount) + 'f', bstr)

        return [traceTitle, cryptoData, samplePoint]

    def setTraceNumber(self, traceNumber):
        self.traceNumber = traceNumber

    def setPointCount(self, pointCount):
        self.pointCount = pointCount

    def setSampleCoding(self, sampleCoding=0, sampleLength=1):
        self.sampleCoding = sampleCoding
        self.sampleLength = sampleLength

    def setDataLength(self, dataLength = 0):
        self.cryptoDataLength = dataLength

    def generateTraceHeader(self):
        traceHeader = b'\x41\x04'
        traceHeader += self.traceNumber.to_bytes(4, 'little')
        traceHeader += b'\x42\x04'
        traceHeader += self.pointCount.to_bytes(4, 'little')
        traceHeader += b'\x43\x01'
        if self.sampleCoding == 0:
            traceHeader += self.sampleLength.to_bytes(1, 'little')
        else:
            traceHeader += (self.sampleLength | 0x10).to_bytes(1, 'little')

        traceHeader += b'\x44\x02'
        traceHeader += self.cryptoDataLength.to_bytes(2,'little')
        traceHeader += b'\x5F\x00'

        self.traceFile.openFile('wb')
        self.traceFile.writeByte(traceHeader)
        self.traceFile.closeFileC()

    def generateTrace(self, point, cryptoData=None, title=None):
        traceStr = b''
        self.traceFile.openFile('ab+')
        if title is not None:
            # traceStr += title.encode('utf8')
            self.traceFile.writeByte(title.encode('utf8'))
        if cryptoData is not None:
            # traceStr += bytes(cryptoData, 'utf8')
            self.traceFile.writeByte(bytes(cryptoData, 'utf8'))
        if self.sampleCoding == 0:
            if self.sampleLength == 1:
                traceStr += bytes(point)
            elif self.sampleLength == 2:
                for i in point:
                    traceStr += pack('<H', i)
            elif self.sampleLength == 4:
                for i in point:
                    traceStr += pack('<I', i)
        else:
            self.traceFile.writeFile(point)
            # for i in point:
            #     # traceStr += pack('<f', i)
            #     self.traceFile.writeByte(pack('<f', i))

        # self.traceFile.writeByte(traceStr)
        self.traceFile.closeFileC()

