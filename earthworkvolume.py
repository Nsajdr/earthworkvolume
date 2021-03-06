#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       earthworkvolume.py
#       
#       Copyright 2010 Javier Rovegno Campos <javier.rovegno@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

class point():
    """
    >>> a = point(0, 0)
    >>> print 'point is %s where x=%s and y=%s'%(a, a.x, a.y)
    point is (0.0, 0.0) where x=0.0 and y=0.0
    """
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return "(%s, %s)"% (self.x, self.y)

    def __str__(self):
        return "(%s, %s)"% (self.x, self.y)


class line():
    """
    >>> a = point(0, 0)
    >>> b = point(3, 3)
    >>> l1 = line(a, b)
    >>> print '%s, m=%s, n=%s'%(l1, l1.m, l1.n) 
    y = 1.0 * x + 0.0, m=1.0, n=0.0
    >>> d = point(4, 5)
    >>> g = point(10, 2)
    >>> l2 = line(d, g)
    >>> print l1 - l2
    y = 1.5 * x + -7.0
    >>> l2.y(4.0) == 5.0
    True
    >>> l2.x(2) == 10.0
    True
    >>> print line(m=0.5,n=2)
    y = 0.5 * x + 2
    >>> l1.area(0.0, 1.0), l2.area(0.0, 1.0)
    (0.5, 6.75)
    """
    def __init__(self, *args, **kargs):
        if args:
            p1 = args[0]
            p2 = args[1]
            if p2.x == p1.x:
                raise ValueError, "x1 must be different of x2"
            self.m = (p2.y - p1.y)/(p2.x - p1.x)
            self.n = p2.y - p2.x * self.m
        elif kargs:
            self.m = kargs['m']
            self.n = kargs['n']
        else:
            raise ValueError, "You must define 2 points or m,n as argument"

    def __repr__(self):
        return "y = %s * x + %s"% (self.m, self.n)

    def __str__(self):
        return "y = %s * x + %s"% (self.m, self.n)

    def __sub__(self, other):
        return line(m=self.m - other.m, n=self.n - other.n)

    def y(self, x):
        return self.m * x + self.n

    def x(self, y):
        return  (y - self.n) / self.m

    def area(self, x1, x2):
        return  (self.y(x1) + self.y(x2))/2.0 * (x2 - x1)


class polyline():
    """
    >>> lx = [0.0,1.0,2.0,3.0]
    >>> ly = [0.0,1.0,0.0,-1.0]
    >>> f = polyline(lx, ly)
    >>> print f.lines
    [y = 1.0 * x + 0.0, y = -1.0 * x + 2.0, y = -1.0 * x + 2.0]
    >>> print f.points
    [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, -1.0)]
    >>> f.y(0.0), f.y(2.0), f.y(3.0)
    (0.0, 0.0, -1.0)
    >>> f.y(0.5), f.y(1.5), f.y(2.5)
    (0.5, 0.5, -0.5)
    >>> f.y(-0.5)
    Traceback (most recent call last):
    ...
    ValueError: x out of range in polyline domain
    >>> f.y(3.5)
    Traceback (most recent call last):
    ...
    ValueError: x out of range in polyline domain
    >>> f.x(0.0), f.x(0.0,1), f.x(-1.0)
    (0.0, 2.0, 3.0)
    >>> f.x(0.5), f.x(0.5, 1, 2), f.x(-0.5)
    (0.5, 1.5, 2.5)
    >>> f.xin(0.0, 0), f.xin(0.0, 1), f.xin(1.9999999999999999, 2)
    (True, False, True)
    >>> f.area(0.0,1.0), f.area(0.0,2.0), f.area(0.0,3.0)
    (0.5, 1.0, 0.5)
    """
    def __init__(self, lx, ly):
        self.lines = []
        self.points = []
        if not isinstance(lx,list):
            raise ValueError, "lx is not a list of x's coordinates of the polyline"
        if not isinstance(lx,list) or not isinstance(ly,list):
            raise ValueError, "ly is not a list of y's coordinates of the polyline"
        if len(lx) != len(ly):
            raise ValueError, "length of len(lx) != len(ly)"
        for i in range(len(lx)):
            self.points.append(point(lx[i], ly[i]))
        for j in range(len(self.points) - 1):
            self.lines.append(line(self.points[j], self.points[j+1]))

    def xin(self, x, j):
        return self.points[j].x <= x <= self.points[j+1].x

    def yin(self, y, j):
        ymin = min(self.points[j].y,self.points[j+1].y)
        ymax = max(self.points[j].y,self.points[j+1].y)
        return ymin <= y <= ymax

    def y(self, x, j=None, n=None):
        if j == None:
            j = 0
        if n == None:
            n = len(self.lines)
        value = None
        while j < n:
            if self.xin(x, j):
                value = self.lines[j].y(x)
                break
            j += 1
        if value == None:
            raise ValueError, "x out of range in polyline domain"
        return value

    def x(self, y, j=None, n=None):
        if j == None:
            j = 0
        if n == None:
            n = len(self.lines)
        value = None
        while j < n:
            if self.yin(y, j):
                value = self.lines[j].x(y)
                break
            j += 1
        if value == None:
            raise ValueError, "y out of range in polyline domain"
        return value

    def area(self, x1, x2):
        """
        x1 inf limit
        x2 sup limit
        """
        if x1 < self.points[0].x:
            raise ValueError, "x values out of range in polyline domain"
        if x2 > self.points[-1].x:
            raise ValueError, "x values out of range in polyline domain"
        value = 0.0
        j = 0
        n = len(self.lines)
        x1pass = False
        while j < n:
            if self.xin(x1, j) and self.xin(x2, j):
                value += self.lines[j].area(x1, x2)
                break
            if x1pass and not self.xin(x2, j):
                value += self.lines[j].area(self.points[j].x, self.points[j+1].x)
            if self.xin(x1, j) and not self.xin(x2, j):
                value += self.lines[j].area(x1, self.points[j+1].x)
                x1pass = True
            if x1pass and self.xin(x2, j):
                value += self.lines[j].area(self.points[j].x, x2)
                break
            j += 1
        return value

    def addline(self, p1, p2):
        # TODO addline at last
        pass

def main():
    pass

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()

