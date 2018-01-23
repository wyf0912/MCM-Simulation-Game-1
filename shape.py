import numpy as np
import math

def circle_h(v):
    r = 0.75
    h = v/(math.pi*r*r)
    return h


def circle_s1(v):
    return math.pi* 2.25/4


def circle_s2(v):
    return math.pi * 0.25


def circle_s3(h):
    return 2*math.pi*0.75*h

def oval(v):
    r = 0.75
    h = v/(math.pi*1.6*0.72*4)
    return h

def oval_s1(h):
    return math.pi* 0.8*0.36

def oval_s2(h):
    return math.pi * 0.65*0.3

def oval_s3(h):
    return math.pi * (1.5(0.8+0.36)-pow(0.8*0.36, 0.5))*h



