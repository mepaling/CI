# coding: utf-8
# pylint: skip-file

from math import *
from exceptions import ZeroDivisionError

class car:
    def __init__(self, x=0, y=0, phi=90, r=3):
        self.x = x
        self.y = y
        self.phi = phi
        self.r = r
        self.sl = 0 # left sensor
        self.sll = line(x, y, slope=-1, xmin=float('-inf'), xmax=0, ymin=0, ymax=float('inf'))
        self.sr = 0 # right sensor
        self.srl = line(x, y, slope=1, xmin=0, xmax=float('inf'), ymin=0, ymax=float('inf'))
        self.sf = 0 # front sensor
        self.sfl = line(x, y, slope=None, xmin=0, xmax=0, ymin=0, ymax=float('inf'))
        self.horaxis = line(x-1.5*r, y, x2=x+1.5*r, y2=y)
        self.veraxis = line(x, y, x2=x, y2=y+1.5*r)
        self.canvas_car = None
        self.canvas_horaxis = None
        self.canvas_veraxis = None
        self.b = r * 2

    def set_pos_direct(self, x, y):
        self.x = x
        self.y = y

    def set_pos_theta(self, theta):
        self.x += cos(degree2radian(self.phi + theta)) + sin(degree2radian(theta)) * sin(degree2radian(self.phi))
        self.y += sin(degree2radian(self.phi + theta)) - sin(degree2radian(theta)) * cos(degree2radian(self.phi))
        self.phi -= radian2degree(asin(2*sin(degree2radian(theta)) / self.b))
        self.sfl = line(self.x, self.y, slope=tan(degree2radian(self.phi)))
        self.sll = line(self.x, self.y, slope=tan(degree2radian(self.phi+45)))
        self.srl = line(self.x, self.y, slope=tan(degree2radian(self.phi-45)))

        #print self.print_sensor()
        if self.phi < -360.0:
            self.phi += 360.0
        elif self.phi > 360.0:
            self.phi -= 360.0

    def set_sensor_val(self, sf, sl, sr):
        self.sf = sf - 3
        self.sl = sl - 3
        self.sr = sr - 3

    def print_car_4D(self, theta=0):
        return ("%.7f %.7f %.7f %.7f" % (self.sf, self.sr, self.sl, theta))

    def print_car_6D(self, theta=0):
        return ("%.7f %.7f %.7f %.7f %.7f %.7f" % (self.x, self.y, self.sf, self.sr, self.sl, theta))
    
    def print_sensor(self):
        return "sfl:" + str(self.sfl) + "\nsrl:" + str(self.srl) + "\nsll:" + str(self.sll)
    
    def __str__(self):
        return ("CAR x:" + str(self.x) + " y:" + str(self.y) + " phi:" + str(self.phi) + " r:" + str(self.r) + 
                " sf:"  + str(self.sf) + " sl:" + str(self.sl) + " sr:" + str(self.sr))


class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def set_point(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return ("x:" + str(self.x) + " y:" + str(self.y))

class line:
    # ax + by + c = 0
    def __init__(self, x1, y1, *args, **kwargs):
        self.point1 = point(x1, y1)
        self.xmin = kwargs.get('xmin')
        self.xmax = kwargs.get('xmax')
        self.ymin = kwargs.get('ymin')
        self.ymax = kwargs.get('ymax')
        if kwargs.get('x2') is not None:
            x2 = kwargs.get('x2')
            y2 = kwargs.get('y2')
            self.point2 = point(x2, y2)
            slope = get_slope(self.point1, self.point2)
            self.slope = slope
            self.a = (y1-y2)
            self.b = (x2-x1)
            self.c = (x1*y2 - y1*x2)
            self.xmin = min(x1, x2)
            self.xmax = max(x1, x2)
            self.ymin = min(y1, y2)
            self.ymax = max(y1, y2)
        else:
            slope = kwargs.get('slope')
            self.slope = slope
            if self.slope is not None:
                self.a = slope
                self.b = -1
                self.c = y1 - slope*x1
            else:
                self.a = 1
                self.b = 0
                self.c = x1

            if self.xmin is None:
                self.xmin = float('-inf')
            if self.xmax is None:
                self.xmax = float('inf')
            if self.ymin is None:
                self.ymin = float('-inf')
            if self.ymax is None:
                self.ymax = float('inf')

    def __str__(self):
        ret = ""
        if not self.a is 0:
            ret += str(self.a) + "x + "
        if not self.b is 0:
            if self.b < 0:
                ret = ret[0:-2]
            ret += str(self.b) + "y + "
        if self.c < 0:
            ret = ret[0:-2]
        ret += str(self.c) + " = 0"
        return ret

def get_slope(p1, p2):
    try:
        return (p1.y - p2.y) / (p1.x - p2.x)
    except ZeroDivisionError:
        return float('inf')
    

def dis_point_line (point, line):
    return (abs(line.a*point.x + line.b*point.y + line.c) / sqrt(line.a*line.a + line.b*line.b))

def dis_p1_p2(p1, p2):
    return sqrt((p2.x-p1.x)*(p2.x-p1.x) + (p2.y-p1.y)*(p2.y-p1.y))

def degree2radian(d):
    return radians(d)

def radian2degree(r):
    return degrees(r)

def point_distance(p, slope, distance):
    deltax = sqrt(distance*distance / (slope*slope + 1))
    deltay = slope*deltax
    return [point(p.x + deltax, p.y+deltay), point(p.x - deltax, p.y-deltay)]

def point_line_interpoint(p, line):
    try:
        x = ( line.b*p.x - line.a*p.y - (line.a*line.c/line.b) ) / ( line.b + (line.a**2 / line.b) )
        y = (-line.a/line.b) * x - (line.c/line.b)
    except ZeroDivisionError:
        return None
    return point(x, y)

# distance between point and line with angle (theta)
def dis_between_point_line_theta(p, li, theta):
    dis = dis_point_line(p, li)
    #print "p:" + str(p) + " line:" + str(li) + " dis:" + str(dis)
    #ans = abs( dis * acos( degree2radian(135-theta) ) )
    ans = abs( dis * (1 / cos( degree2radian(theta) + (degree2radian(90)-atan(li.slope)) )) )
    ip = point_line_interpoint(p, li)
    if ip is not None:
        if not (li.xmin <= ip.x and ip.x <= li.xmax and li.ymin <= ip.y and ip.y <= li.ymax):
            return float('inf')
    return ans

# Cramer's rule
def point_intersection_between_lines(line1, line2):
    delta = line1.a*line2.b - line1.b*line2.a
    deltax = -line1.c*line2.b + line1.b*line2.c
    deltay = -line1.a*line2.c + line1.c*line2.a
    if delta is not 0:
        return point(deltax / delta, deltay / delta)
    elif delta is 0 and deltax and 0 and deltay and 0:
        return float('inf')
    else:
        return None

# True if n is between a and b ()
def between_ab(n, a, b):
    if a <= n and n <= b:
        return True
    return False
