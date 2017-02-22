

class MyUtil(object):
    def calHW(self, data):
        ans = 0
        while data:
            data &= data - 1
            ans += 1
        return ans
