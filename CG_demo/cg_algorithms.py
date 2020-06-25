#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math


def sign(x):
    if x < 0: 
        return -1
    elif x == 0:
        return 0
    elif x > 0:
        return 1
        
def draw_line(p_list, algorithm):
    """绘制线段

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    if algorithm == 'Naive':
        if x0 == x1:
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)
            for x in range(x0, x1 + 1):
                result.append((x, int(y0 + k * (x - x0))))
    elif algorithm == 'DDA':
        if abs(x1 - x0) >= abs(y1 - y0):
            length = abs(x1 - x0) * 1.0
        else:
            length = abs(y1 - y0) * 1.0
        if length == 0:
            return result
        delt_x = (x1 - x0) / length
        delt_y = (y1 - y0) / length
        x = x0 + 0.5
        y = y0 + 0.5
        i = 1
        while i <= length:
            result.append((math.floor(x), math.floor(y)))
            x = x + delt_x
            y = y + delt_y
            i = i + 1
    elif algorithm == 'Bresenham':
        x = x0
        y = y0
        delta_x = abs(x1 - x0)
        delta_y = abs(y1 - y0)
        s1 = sign(x1 - x0)
        s2 = sign(y1 - y0)
        if delta_y > delta_x:
            temp = delta_x
            delta_x = delta_y
            delta_y = temp
            interchange = 1
        else:
            interchange = 0
        e = 2 * delta_y - delta_x
        for i in range (1, delta_x + 1):
            result.append((x, y))
            while e > 0:
                if interchange == 1:
                    x = x + s1
                else:
                    y = y +s2
                e = e - 2 * delta_x
            if interchange == 1:
                y = y + s2
            else:
                x = x + s1
            e = e + 2 * delta_y
    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形 

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    " TODO: boundary bug "
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    return result

class Node:
    def __init__(self, x = 0.0, dx = 0.0, ymax = 0.0, next = None):
        self.x = x
        self.dx = dx
        self.ymax = ymax
        self.next = next
    def getX(self):
        return self.x
    def getDx(self):
        return self.dx
    def getYmax(self):
        return self.ymax
    def getNext(self):
        return self.next
    def setX(self, temp):
        self.x = temp
    def setDx(self, temp):
        self.dx = temp
    def setYmax(self, temp):
        self.ymax = temp
    def setNext(self, temp):
        self.next = temp
    
def fill(p_list):
    """fill polygon
    
    : param p_list (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    vertNum = len(p_list)
    MaxY = 0
    MinY = 2000
    for i in range(vertNum):
        x0, y0 = p_list[i]
        if y0 < MinY:
            MinY = y0
        if y0 > MaxY:
            MaxY = y0
    pAET = Node()
    pAET.setNext(None)
    pNet = []
    for i in range(0, MaxY + 1):
        temp = Node()
        temp.setDx(0)
        temp.setX(0)
        temp.setYmax(0)
        temp.setNext(None)
        pNet.append(temp)
    
    for i in range(MinY, MaxY + 1):
        for j in range(0, vertNum):
            if p_list[j][1] == i:
                x0, y0 = p_list[j]
                x1, y1 = p_list[(j - 1 + vertNum) % vertNum]
                if y1 > y0:
                    temp = Node()
                    temp.setX(x0)
                    temp.setYmax(y1)
                    temp.setDx(1.0 * (x1 - x0) / (y1 - y0))
                    temp.setNext(pNet[i].getNext())
                    pNet[i].setNext(temp)
                x1, y1 = p_list[(j + 1 + vertNum) % vertNum]
                if y1 > y0:
                    temp = Node()
                    temp.setX(x0)
                    temp.setYmax(y1)
                    temp.setDx(1.0 * (x1 - x0) / (y1 - y0))
                    temp.setNext(pNet[i].getNext())
                    pNet[i].setNext(temp)
   
    for i in range(MinY, MaxY + 1):
        p = pAET.getNext()
        while p != None:
            p.setX(p.getX() + p.getDx())
            p = p.getNext()
        
        tq = pAET
        p = pAET.getNext()
        tq.setNext(None)
        while p != None:
            while tq.getNext() != None and p.getX() >= tq.getNext().getX():
                tq = tq.getNext()
            s = p.getNext()
            p.setNext(tq.getNext())
            tq.setNext(p)
            p = s
            tq = pAET
        
        q = pAET
        p = q.getNext()
        while p != None:
            if p.getYmax() == i:
                q.setNext(p.getNext())
                p = q.getNext()
            else:
                q = q.getNext()
                p = q.getNext()
        
        p = pNet[i].getNext()
        q = pAET
        while p != None:
            while q.getNext() != None and p.getX() >= q.getNext().getX():
                q = q.getNext()
            s = p.getNext()
            p.setNext(q.getNext())
            q.setNext(p)          
            p = s
            q = pAET
            
        p = pAET.getNext()
        while p != None and p.getNext() != None:
            j = p.getX()
            while j <= p.getNext().getX():
                result.append((int(j), i))
                j = j + 1
            p = p.getNext().getNext()
    return result
    
def draw_ellipse(p_list):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    xc = (x0 + x1) / 2
    yc = (y0 + y1) / 2
    a = (x1 - x0) / 2
    b = (y1 - y0) / 2
    d = b * b + a * a * (0.25 - b)
    x = 0
    y = b
    
    result.append((xc + x, yc + y))
    result.append((xc + x, yc - y))
    result.append((xc - x, yc - y))
    result.append((xc - x, yc + y))
    
    while b * b * (x + 1) < a * a * (y - 0.5):
        if d < 0:
            d = d + b * b * (2 * x + 3)
        else:
            d = d + b * b * (2 * x + 3) + a * a * ((-2) * y + 2)
            y = y - 1
        x = x + 1
        result.append((xc + x, yc + y))
        result.append((xc + x, yc - y))
        result.append((xc - x, yc - y))
        result.append((xc - x, yc + y))

    while y > 0:
        if d < 0:
            d = d + b * b * (2 * x + 2) + a * a * ((-2) * y + 3)
            x = x + 1
        else:
            d = d + a * a * ((-2) * y + 3)
        y = y - 1
        result.append((xc + x, yc + y))
        result.append((xc + x, yc - y))
        result.append((xc - x, yc - y))
        result.append((xc - x, yc + y))
   
    return result
   

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
    
    
def binomial(n, i):
    a = factorial(n)
    b = factorial(i) * factorial(n - i)
    return a / b
    
    
def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    if algorithm == 'Bezier':
        n = len(p_list) - 1
        for i in range(0, 10000):
            t = i / 10000.0
            x = 0
            y = 0
            for j in range(len(p_list)):
                x0, y0 = p_list[j]
                p = binomial(n, j)
                x = x + p * x0 * math.pow(t, j) * math.pow(1 - t, n - j)
                y = y + p * y0 * math.pow(t, j) * math.pow(1 - t, n - j) 
            result.append((int(x),int(y)))
    else:
        for i in range(len(p_list) - 3):
            delta = 0.0001
            t = 0
            while t <= 1:
                b0 = 1 / 6.0 * (1 - t) * (1 - t) * (1 - t)
                b1 = 1 / 6.0 * (3 * t * t * t - 6 * t * t + 4)
                b2 = 1 / 6.0 * ((-3) * t * t * t + 3 * t * t + 3 * t + 1)
                b3 = 1 / 6.0 * t * t * t
                x1, y1 = p_list[i]
                x2, y2 = p_list[i + 1]
                x3, y3 = p_list[i + 2]
                x4, y4 = p_list[i + 3]
                x = b0 * x1 + b1 * x2 + b2 * x3 + b3 * x4
                y = b0 * y1 + b1 * y2 + b2 * y3 + b3 * y4
                result.append((int(x), int(y)))
                t = t + delta
        
    return result


def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    for i in range(len(p_list)):
        x0, y0 = p_list[i]
        x0 = x0 + dx
        y0 = y0 + dy
        result.append((x0, y0))
    return result

def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    sint = math.sin(math.pi * r / 180)
    cost = math.cos(math.pi * r / 180)
    for i in range(len(p_list)):
        x0, y0 = p_list[i]
        x1 = x + (x0 - x) * cost - (y0 - y) * sint
        y1 = y + (x0 - x) * sint + (y0 - y) * cost
        result.append((int(x1), int(y1)))
    return result


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    for i in range(len(p_list)):
        x0, y0 = p_list[i]
        x1 = x0 * s + x * (1 - s)
        y1 = y0 * s + y * (1 - s)
        result.append((int(x1), int(y1)))
    return result

def getCode(x, y, x_min, y_min, x_max, y_max):
    code = 0
    if x < x_min:
        code = code | 0x01
    else:
        code = code & 0xfe
    
    if x > x_max:
        code = code | 0x02
    else:
        code = code & 0xfd
    
    if y < y_min:
        code = code | 0x04
    else:
        code = code & 0xfb
    
    if y > y_max:
        code = code | 0x08
    else:
        code = code & 0xf7
    return code
    
u1 = 0.0
u2 = 1.0
def clipTest(p, q):
    global u1, u2
    flag = True
    if p < 0.0:
        r = q * 1.0 / p
        if r > u2:
            flag = False
        elif r > u1:
            u1 = r
            flag = True
    elif p > 0:
        r = q * 1.0 / p
        if r < u1:
            flag = True
        elif r < u2:
            u2 = r
            flag = True
    elif q < 0:
        flag = False
    return flag
    
def clip(p_list, x_min, y_min, x_max, y_max, algorithm):
    """线段裁剪

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标
    :param algorithm: (string) 使用的裁剪算法，包括'Cohen-Sutherland'和'Liang-Barsky'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1]]) 裁剪后线段的起点和终点坐标
    """
    result = []
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    if algorithm == 'Cohen-Sutherland':
        done = False
        c1 = getCode(x0, y0, x_min, y_min, x_max, y_max)
        c2 = getCode(x1, y1, x_min, y_min, x_max, y_max)
        while not done:
            if c1 == 0 and c2 == 0:
                result.append((x0, y0))
                result.append((x1, y1))
                done = True
            elif c1 & c2 != 0:
                result.append((0, 0))
                result.append((0, 0))
                done = True
            else:
                if c1 != 0:
                    code = c1
                else: 
                    code = c2
                if code & 0x01 != 0:
                    x = x_min
                    m = (y1 - y0) / (x1 - x0)
                    y = y0 + int((x - x0) * m)
                elif code & 0x08 != 0:
                    y = y_max
                    m = (x1 - x0) / (y1 - y0)
                    x = x0 + int((y - y0) * m)
                elif code & 0x02 != 0:
                    x = x_max
                    m = (y1 - y0) / (x1 - x0)
                    y = y0 + int((x - x0) * m)
                elif code & 0x04 != 0:
                    y = y_min
                    m = (x1 - x0) / (y1 - y0)
                    x = x0 + int((y - y0) * m)
                if code == c1:
                    x0 = x
                    y0 = y
                    c1 = getCode(x0, y0, x_min, y_min, x_max, y_max)
                else:
                    x1 = x
                    y1 = y
                    c2 = getCode(x1, y1, x_min, y_min, x_max, y_max)
    else:
        dx = x1 - x0
        global u1, u2
        u1 = 0.0
        u2 = 1.0
        if  clipTest(-dx, x0 - x_min):
            if clipTest(dx, x_max - x0):
                dy = y1 - y0
                if clipTest(-dy, y0 - y_min):
                    if clipTest(dy, y_max - y0):
                        x = x0 + u1 * dx
                        y = y0 + u1 * dy
                        result.append((int(x), int(y)))
                        x = x0 + u2 * dx
                        y = y0 + u2 * dy
                        result.append((int(x), int(y)))
                        return result
        result.append((0, 0))
        result.append((0, 0))
    return result

class Vector:
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0 * 1.0
        self.y0 = y0 * 1.0
        self.x1 = x1 * 1.0
        self.y1 = y1 * 1.0
    def getX0(self):
        return self.x0
    def getY0(self):
        return self.y0
    def getX1(self):
        return self.x1
    def getY1(self):
        return self.y1

def Multi(x, y, x0, y0, x1, y1):
    return ((x0 - x) * (y1 - y) - (x1 - x) * (y0 - y))
    
def isInside(x, y, v):
    if Multi(x, y, v.getX0(), v.getY0(), v.getX1(), v.getY1()) >= 0:
        return True
    else:
        return False

def InterSection(S, p, v):
    x0, y0 = S
    x1, y1 = p
    x2 = v.getX0()
    y2 = v.getY0()
    x3 = v.getX1()
    y3 = v.getY1()
    
    t1 = Multi(x0, y0, x3, y3, x2, y2)
    t2 = Multi(x1, y1, x3, y3, x2, y2)
    pX = (t1 * x1 - t2 * x0) / (t1 - t2)
    pY = (t1 * y1 - t2 * y0) / (t1 - t2)
    return (pX, pY)
    
def pclip(p_list, x_min, y_min, x_max, y_max):
    """多边形裁剪

    :param p_list (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标
    :return: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 裁剪后多边形的顶点坐标列表
    """
    result = []
    vectors = []
    cur = []
    vectors.append(Vector(x_max, y_min, x_max, y_max))
    vectors.append(Vector(x_max, y_max, x_min, y_max))
    vectors.append(Vector(x_min, y_max, x_min, y_min))
    vectors.append(Vector(x_min, y_min, x_max, y_min))
    
    pointSize = len(p_list)
    S = p_list[pointSize - 1]
    for i in range(0, pointSize):
        x0, y0 = p_list[i]
        result.append((x0 * 1.0, y0 * 1.0))
    
    for j in range(0, 4):
        if isInside(S[0], S[1], vectors[j]):
            flag = False
        else:
            flag = True
        resultSize = len(result)
        for i in range(0, resultSize):
            x0, y0 = result[i]
            if isInside(x0, y0, vectors[j]):
                if flag:
                    flag = False
                    cur.append(InterSection(S, result[i], vectors[j]))
                cur.append(result[i])  
            else:
                if flag == False:
                    flag = True
                    cur.append(InterSection(S, result[i], vectors[j]))
            S = result[i]
        result = cur
        cur = []
    
    ans = []
    for i in range(len(result)):
        x0, y0 = result[i]
        ans.append((int(x0), int(y0)))
    return ans