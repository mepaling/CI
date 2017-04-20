# pylint: skip-file

from enum import Enum

class Degree(Enum):
    NS = -1
    PS = 1
    NM = -2
    PM = 2
    NL = -3
    PL = 3
    AZ = 0

class FuzzySystem:
    fuzzyi = 0
    def fuzzy_main(self, sf, sl, sr):
        funVal = [55, -55, -40.0, 40.0, 30, -30]
        a = [self.membership_sl(sl, Degree.PM), self.membership_sr(sr, Degree.PM),
             self.membership_sr(sr, Degree.PS), self.membership_sl(sl, Degree.PS),
             self.membership_sf(sf, Degree.PM) * self.membership_sr(sr, Degree.AZ), self.membership_sf(sf, Degree.PM) * self.membership_sl(sl, Degree.AZ)]
        val = max(min(40, self.weightedAverage(a, funVal)), -40)
        #return val
        #return 0
        return self.fuzzy2()

    def weightedAverage(self, a, funVal):
        A = 0
        B = 0
        for i in range(len(a)):
            A += a[i] * funVal[i]
            B += a[i]
        if abs(B) < 1e-6:
            return 0
        return A / B

    def membership_sf(self, sf, degree):
        if degree is Degree.AZ:
            if sf < 3:
                return 1
            if sf < 10:
                return -sf / 7.0 + 10.0 / 7.0
            return 0
        elif degree is Degree.PS:
            if sf < 30:
                return 0
            return 1
        elif degree is Degree.PM:
            if sf < 30:
                return 0
            return 1
        else:
            return 0
        
    def membership_sr(self, sr, degree):
        if degree is Degree.AZ:
            if sr < 4:
                return 1
            if sr < 5:
                return -sr + 5
            return 0
        elif degree is Degree.PS:
            if sr < 4:
                return 0
            if sr < 10:
                return  sr / 6 - 4 / 6.0
            if sr < 16:
                return -sr / 6 + 16 / 6.0
            return 0
        elif degree is Degree.PM:
            
            if sr < 8:
                return 0
            if sr < 16:
                return sr / 8 - 1
            return 1
        else:
            return 0
        
    def membership_sl(self, sl, degree):
        if degree is Degree.AZ:
            if sl < 4:
                return 1
            if sl < 5:
                return -sl + 5
            return 0
        elif degree is Degree.PS:
            if sl < 4:
                return 0
            if sl < 10:
                return sl / 6 - 4 / 6.0
            if sl < 16:
                return -sl / 6 + 16 / 6.0
            return 0
        elif degree is Degree.PM:
            if sl < 10:
                return 0
            if sl < 16:
                return sl / 6 - 10 / 6.0
            return 1
        else:
            return 0

    def fuzzy2(self):
        fuzzy_arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 40, 40, 40, 30,30,30,30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 -40, -40, -30,-20, -20, -20, -20, -20, -10, -10, 0, 0, 0, 0]
        fuzzy_arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 40, 40, 40, 30,30,30,30, 20, 20, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -40, -40, -30, -30, -30, -30,-20, -20, -20, -10, -10, -10, -10, 0, 0, 0, 0, 0, 0, 0]
        fuzzy_arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 40, 40, 40, 40, 40, 40, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -40, -40, -40, -40, -40, -40, -40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        result = fuzzy_arr[self.fuzzyi % len(fuzzy_arr)]
        self.fuzzyi += 1
        return result
